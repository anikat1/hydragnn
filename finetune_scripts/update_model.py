import torch.nn as nn
def create_mlps(config):
    """
    Creates head MLPs that take input from a pretrained shared layer.
    
    Args:
        config (dict): A dictionary with the following keys:
            - dim_pretrained (int): Dimension of the pretrained shared layer output.
            - dim_headlayers (list of int): List containing the dimensions for layers within each head.
            - output_dim (list of int): List containing the output dimensions for each head.

    Returns:
        list of nn.Sequential: A list of head MLP modules.
    """
    dim_pretrained = config['output_heads']['graph']["dim_pretrained"]
    dim_headlayers = config['output_heads']['graph']["dim_headlayers"]
    output_dims = config["output_dim"]

    # Create head MLPs
    head_mlps = []
    for head_index in range(len(output_dims)):
        head_layers = []
        in_dim = dim_pretrained  # Use pretrained layer dimension as input
        
        # Create hidden layers based on dim_headlayers
        for head_dim in dim_headlayers:
            head_layers.append(nn.Linear(in_dim, head_dim))
            head_layers.append(nn.ReLU())
            in_dim = head_dim

        # Output layer for each head with specified output dimension
        head_layers.append(nn.Linear(in_dim, output_dims[head_index]))

        # Create the head MLP as a Sequential model
        head_mlp = nn.Sequential(*head_layers)
        head_mlps.append(head_mlp)

    return nn.ModuleList(head_mlps)

def update_model(model, ft_config):
    import pdb
    device = next(model.parameters()).device
    head_mlps = create_mlps(ft_config['FTNeuralNetwork']['Architecture'])
    model.heads_NN = head_mlps.to(device)
    #pdb.set_trace()
    model.head_type = ft_config['FTNeuralNetwork']['Architecture']["output_heads"]["graph"]["num_headlayers"]*["graph"]
    model.head_dims = ft_config['FTNeuralNetwork']['Architecture']["output_dim"]
    model.loss_weights = ft_config['FTNeuralNetwork']['Architecture']['task_weights'] 
    model.num_heads = len(head_mlps)
    # model.module.heads_NN = head_mlps.to(device)
    # model.module.head_type = ft_config['FTNeuralNetwork']['Architecture']["output_heads"]["graph"]["num_headlayers"]*["graph"]
    # model.module.head_dims = ft_config['FTNeuralNetwork']['Architecture']["output_dim"]
    # model.module.num_heads = len(head_mlps)
    
    # to do: modify losses 
    return model
