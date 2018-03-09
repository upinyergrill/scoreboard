#from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from multiprocessing import Process, Queue

# The REST API
def rest_api(rest_api_queue):
    ''' This will use Flask REST API
        At a bare minimum it will have a route called
        /team/:id where you can post to the int value
        for the team that you would like to display
        When a valid team id is matched, then it will send
        a message via the rest_api_queue to the Board process '''
    pass

# The Board
def board(rest_api_queue):
    ''' This will need to listen to the rest_api_queue 
    for messages to switch teams and things like that '''
    
    ''' This process need to have a sub prrocess for 
        getting game data, it will call both 
        the "next" and the "live" data URIs '''
    
    # Create Fetch NHL Data proces
    fetch_nhl_data_process = Process(target=fetch_nhl_data, args=())
    
    # Start Fetch NHL Data process
    fetch_nhl_data_process.start()
    
    # Wait for Fetch NHL Data to finish (it never will)
    #fetch_nhl_data_process.join()
    
    ''' The main function of the Board process should be waiting
        for the REST API process to send it data
        
        The process should also handle starting and stopping
        all the other sub processes for 
        getting and display data on the board '''
    while True:
        try:
            message_from_rest_api = rest_api_queue.get(False)
            ''' Need a function for processing the data from the rest api
                Probably should send an object from the rest api of the
                function and the value
                something like... 
                    {
                        "function": "changeTeam"
                        "value": 17
                    } 
                Changing the team will need to tell the fetch_nhl_data
                function to use a differnt URIs but also will need to
                tell the function for what colors to use to update. '''
        except:
            pass
    pass

# Download NHL Data
def fetch_nhl_data():
    ''' download data from the "next" URI and
        download data fro mthe "live" URI. '''
    pass

def determine_game_state():
    ''' This function determines the state of the game.
        The possible states are, pre, live, and post. '''
    # Download "next" URI
    # Find the next/current game from the "next" data
    # Download "live" URI
    # if game is live
        #  display live game data
    # else
        # if (the game has ended within the last 15 minutes)
            # display post game
        # if else (the next game starts in 15 minutes or less)
            # display pre game
        # else (if the game has ended more than 15 minutes ago, 
        # and the next game doesn't start in 15 minutes or less)
            # turn off the board display 
    pass

# This is the main process
if __name__ == '__main__':
    # Queue for the REST API to send infomration to the Board process
    rest_api_queue = Queue()

    # Create the REST API process
    rest_api_process = Process(target=rest_api, args=(rest_api_queue,))
    
    # Create the Board process
    board_process = Process(target=board, args=(rest_api_queue,))
    
    # Start the REST API
    rest_api_process.start()

    # Start the Board
    board_process.start()

    # Wait for the REST API to finsih (it never will)
    rest_api_process.join()

    # Wait for the Board to finsih (it never will)
    board_process.join()
