import json

from swarm import Swarm
'''
这个文件实现了一个交互式的命令行界面（REPL - Read-Eval-Print Loop）用于 Swarm 系统。主要包含以下几个关键功能：

1. 处理和打印流式响应：process_and_print_streaming_response 函数用于处理和打印 Swarm 的流式响应。
2. 美化打印消息历史：pretty_print_messages 函数用于美化打印 Swarm 的消息历史。
3. 运行交互式循环：run_demo_loop 函数用于运行 Swarm 的交互式循环。
'''

def process_and_print_streaming_response(response):
    """
    处理和打印流式响应
    
    参数:
        response: 流式响应对象
    
    返回:
        response: 如果存在完整响应则返回，否则为None
    """
    content = ""  # 存储当前消息内容
    last_sender = ""  # 存储最后发送者

    for chunk in response:
        # 处理发送者信息
        if "sender" in chunk:
            last_sender = chunk["sender"]

        # 处理内容块
        if "content" in chunk and chunk["content"] is not None:
            # 如果是新消息，先打印发送者名称
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            # 打印内容并累加到content中
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]

        # 处理工具调用
        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                # 打印工具调用信息（紫色显示）
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        # 处理消息结束标记
        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # 消息结束换行
            content = ""

        # 返回完整响应（如果存在）
        if "response" in chunk:
            return chunk["response"]


def pretty_print_messages(messages) -> None:
    """
    美化打印消息历史
    
    参数:
        messages: 消息历史列表
    """
    for message in messages:
        # 只处理助手的消息
        if message["role"] != "assistant":
            continue

        # 蓝色打印代理名称
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # 打印响应内容
        if message["content"]:
            print(message["content"])

        # 打印工具调用（如果有）
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            # 格式化参数显示
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            # 紫色显示函数名
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")


def run_demo_loop(
    starting_agent, context_variables=None, stream=False, debug=False
) -> None:
    """
    运行交互式命令行界面
    
    参数:
        starting_agent: 初始代理
        context_variables: 上下文变量字典
        stream: 是否使用流式输出
        debug: 是否启用调试模式
    """
    # 初始化Swarm客户端
    client = Swarm()
    print("Starting Swarm CLI 🐝")

    # 初始化消息历史和当前代理
    messages = []
    agent = starting_agent

    # 主交互循环
    while True:
        # 获取用户输入
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})

        # 运行Swarm代理
        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            debug=debug,
        )

        # 根据stream参数选择不同的输出处理方式
        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        # 更新消息历史和当前代理
        messages.extend(response.messages)
        agent = response.agent
