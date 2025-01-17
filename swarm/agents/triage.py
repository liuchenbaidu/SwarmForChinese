from swarm import Agent

def create_triage_agent(name="Triage Agent", instructions=None, agents=None, add_backlinks=True):
    """
    创建分诊代理
    
    参数:
        name: 代理名称
        instructions: 代理指令
        agents: 可用的代理列表
        add_backlinks: 是否添加返回链接
    """
    if agents is None:
        agents = []
        
    if instructions is None:
        instructions = """You are to triage a users request, and call a tool to transfer to the right intent.
        Once you are ready to transfer to the right intent, call the tool to transfer to the right intent."""
    
    # 创建转移到其他代理的函数
    def create_transfer_function(target_agent):
        def transfer():
            return target_agent
        transfer.__name__ = f"transfer_to_{target_agent.name.lower().replace(' ', '_')}"
        return transfer
    
    # 为每个代理创建转移函数
    functions = [create_transfer_function(agent) for agent in agents]
    
    return Agent(
        name=name,
        instructions=instructions,
        functions=functions
    ) 