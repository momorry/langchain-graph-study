from typing import TypedDict, Literal, Sequence

from langchain_core.messages import HumanMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send

from study.base.model.chat_model import get_model

# 初始化大语言模型
model = get_model()


# ==================== 状态定义 ====================

# 1. 全局状态 (OverAllState)：整个图运行期间共享的状态
#    - topic: 用户输入的主题
#    - pome: 存储生成的七言绝句
#    - ci_pome: 存储生成的词
#    - joke: 存储生成的笑话
class OverAllState(TypedDict):
    topic: str
    pome: str
    ci_pome: str
    joke: str


# 2. 私有状态 (wokerState)：每个并行工作节点独立使用的输入状态
#    - content_type: 标识当前任务类型（诗/词/笑话），用于决定结果写入哪个字段
#    - prompt: 发送给模型的完整提示词
class wokerState(TypedDict):
    content_type: Literal['pome', 'joke', 'ci_pome']
    prompt: str


# 3. 输入状态 (inputState)：图启动时从外部接收的初始输入
#    - topic: 用户提供的主题，例如"山峦"
class inputState(TypedDict):
    topic: str


# 4. 输出状态 (outputState)：图执行完成后返回的最终结果
#    - poem: 七言绝句
#    - ci_pome: 词
#    - joke: 笑话
class outputState(TypedDict):
    poem: str
    ci_pome: str
    joke: str


# ==================== 节点定义 ====================

# 工作节点：接收私有状态，调用大模型生成内容，返回结果
# 由于通过 Send 分发，多个 woker_node 实例可以并行执行
def woker_node(state: wokerState) -> outputState:
    content_type = state['content_type']
    prompt = state['prompt']
    # 调用模型生成内容，并提取返回消息中的文本
    content = model.invoke([HumanMessage(prompt)]).content
    print(f"content:{content}")
    return {
        # 根据 content_type 动态决定写入哪个字段（pome / ci_pome / joke）
        content_type: content
    }


# ==================== 路由函数 ====================

# 路由函数：根据输入主题，动态生成 3 个 Send 任务，实现并行调用
# 返回 Send 列表后，LangGraph 会为每个 Send 创建一个独立的 woker_node 实例并行执行
def router(state: inputState) -> Sequence[Send]:
    router_prompt = "请生成一首关于{}的{}"
    # 中英文映射：将内部标识转换为中文创作类型
    english2Chinese = {
        "pome": "七言绝句",
        "ci_pome": "词",
        "joke": "笑话"
    }
    topic = state['topic']
    # 为每种 content_type 创建一个 Send，分发到同一个 woker_node 节点
    # 每个 Send 携带独立的私有状态（content_type 和 prompt）
    return [
        Send(
            "woker_node",  # 目标节点名称
            {              # 传递给目标节点的私有状态
                "content_type": content_type,
                "prompt": router_prompt.format(topic, english2Chinese[content_type])
            }
        )
        for content_type in ["pome", "ci_pome", "joke"]
    ]


# ==================== 构建与编译图 ====================

# 创建状态图，指定全局状态、输入状态和输出状态的 Schema
builder = StateGraph(state_schema=OverAllState, input_schema=inputState, output_schema=outputState)

# 添加工作节点
builder.add_node("woker_node", woker_node)

# 添加条件边：从 START 出发，由 router 函数决定动态分发到哪些节点
# path_map 用于映射 router 返回的 Send 目标到实际节点名
builder.add_conditional_edges(START, router, path_map={"woker_node": "woker_node"})

# 工作节点执行完成后，统一流向 END
builder.add_edge("woker_node", END)

# 编译图
graph = builder.compile()

# ==================== 执行图 ====================

# 启动图，传入主题"山峦"
res = graph.invoke({"topic": "山峦"})

# 打印最终结果：包含一首七言绝句、一首词和一个笑话
print(res)

#总结：通过Send可以实现动态扇出
# 1. 动态任务分发
# 运行时根据条件决定发送多少个任务，而不是在编译时写死。例如代码中根据 content_type 列表动态生成 3 个任务——如果主题不同，任务数量完全可以动态变化。
# 2. 真正的并行执行
# 返回多个 Send 后，LangGraph 会为每个 Send 创建独立的节点实例并行运行，显著缩短总耗时。3 个 AI 生成任务同时进行，而不是串行等待。
# 3. 独立的私有状态隔离
# 每个 Send 可以携带独立的输入状态（wokerState），各任务之间互不干扰。代码中每个 woker_node 收到不同的 content_type 和 prompt，彼此完全隔离。
# 4. 灵活的 Map-Reduce 模式
# 天然支持"先拆分(Map) → 并行处理 → 再聚合(Reduce)"的复杂工作流。适合批量数据处理、多维度内容生成、分片计算等场景。