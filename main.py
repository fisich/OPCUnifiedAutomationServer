from OPCUAServer import OPCUAServerManager
from variable_manipulations import update_vars
import asyncio
from asyncua import ua

variables = list()


async def main():
    global variables
    server_manager = OPCUAServerManager()
    await server_manager.create_server("opc.tcp://0.0.0.0:4840/", "Fisenko OPC UA Server")
    node_1 = await server_manager.add_node("Node 1")
    node_2 = await server_manager.add_node("Node 2")
    variables = list()
    # First node variables
    await server_manager.add_variable_to_object(node_1, "Variable_sin_1", 1, ua.VariantType.Double,
                                                OPCUAServerManager.read_attributes)
    await server_manager.add_variable_to_object(node_1, "Variable_inc_2", 100, ua.VariantType.Int64,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.write_attributes)
    await server_manager.add_variable_to_object(node_1, "Variable_inc_3", 100000000, ua.VariantType.Int64,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.write_attributes)
    await server_manager.add_variable_to_object(node_1, "Variable_randtext_4", "text", ua.VariantType.String,
                                                OPCUAServerManager.read_attributes)
    await server_manager.add_variable_to_object(node_1, "Variable_cos_5", 1, ua.VariantType.Double,
                                                OPCUAServerManager.read_attributes)
    variables.extend(await node_1.get_variables())
    # Folder for second node
    folder_1 = await server_manager.add_folder_to_object(node_2, "Folder 1")
    # Variable for folder of second node
    await server_manager.add_variable_to_object(folder_1, "Variable_sin_6", 1, ua.VariantType.Double,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.history_attributes)

    await server_manager.add_variable_to_object(folder_1, "Variable_inc_7", -10000000, ua.VariantType.Int64,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.write_attributes +
                                                OPCUAServerManager.history_attributes)

    await server_manager.add_variable_to_object(folder_1, "Variable_inc_8", 1.000000000001, ua.VariantType.Double,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.history_attributes)

    await server_manager.add_variable_to_object(folder_1, "Variable_cos_9", 1, ua.VariantType.Double,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.history_attributes)

    await server_manager.add_variable_to_object(folder_1, "Variable_randtext_10", "text", ua.VariantType.String,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.history_attributes)
    variables.extend(await folder_1.get_variables())
    # Variable for second node
    await server_manager.add_variable_to_object(node_2, "Variable_inc_11", 1, ua.VariantType.Int64,
                                                OPCUAServerManager.read_attributes + OPCUAServerManager.write_attributes)
    variables.extend(await node_2.get_variables())
    await server_manager.server.start()
    await server_manager.activate_historizing_for_variables(await folder_1.get_variables())

    asyncio.get_event_loop().create_task(update_vars(variables))
    while True:
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())
