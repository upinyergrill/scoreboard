from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
import json
import nhl_board_render as nhlboardrender
from matrix_thread import ScrollNextGameThread, CarouselThread
from multiprocessing import Value

# The Board
def board(rest_api_queue, shared_board_state, shared_board_brightness, font, team_colors):
    ''' The main function of the Board process should be waiting
        for the REST API process to send it data
        
        The process should also handle starting and stopping
        all the other sub processes for 
        getting and display data on the board '''
    # Create the process for running the board
    #rest_api_queue = Queue()
    #board_process = Process(target=board, args=(rest_api_queue,))
    #board_process.start()

    # Things that wont change on board
    color_white = graphics.Color(255, 255, 255)

    # Keep track of game state
    # this way we can clear the board to get ready for a new view
    current_game_state = None

    # init for if statment
    game_data = {}

    while True:
        # init board state
        current_board_state = shared_board_state.value
        # Init brightness from shared mem
        current_brightness = shared_board_brightness.value

        # RGBMatrix Options
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.brightness = current_brightness * 20
        options.gpio_slowdown = 2
        options.drop_privileges = 0

        # Create matrix with optiosn
        matrix = RGBMatrix(options = options)

        print('the board started')

        while True:
            try:
                # init for break
                # This gives a new shared memory object
                # per run of the loop.
                break_scroll_thread = Value('i', False)
                break_carousel_thread = Value('i', False)

                if game_data:
                    
                    # We will hold on to this game_data incase we break from this looop
                    # to reallocate the matrix with a new brightness, and we can rerender
                    # the data before we start waiting for new data
                    #current_game_data = game_data
                    # If brightness changes, re-render the board
                    if (current_brightness != shared_board_brightness.value):
                        # matrix __dealloc__
                        matrix = None
                        break
                    
                    
                    current_brightness = shared_board_brightness.value

                    print('board got game data')
                    #print(game_data)
                    print('current_board_state', current_board_state)
                    print('shared_board_state', shared_board_state.value)
                    # Clear the board, but only clear if the state has changed from 1 to 0
                    if (current_board_state == 1 and shared_board_state.value == 0):
                        matrix.Clear()
                    elif (current_board_state == 0 and shared_board_state.value ==0):
                        # The board is off, leave it offs
                        pass
                    else:
                        # Check if the game state has changed
                        # life cylce
                        # preview -> live   | Clear
                        # live -> final     | Don't clear
                        # final -> preview  | Clear
                        if (current_game_state is not None):
                            if (current_game_state == "Preview" and game_data['gameState'] == "Live"):
                                matrix.Clear()
                            elif (current_game_state == "Live" and game_data['gameState'] == "Final"):
                                pass
                            if (current_game_state == "Final" and game_data['gameState'] == "Preview"):
                                matrix.Clear()

                        current_game_state = game_data['gameState']

                        #print(team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
                        team_color = {
                            'r': team_colors[str(game_data['currentTeamId'])]['r'],
                            'g': team_colors[str(game_data['currentTeamId'])]['g'],
                            'b': team_colors[str(game_data['currentTeamId'])]['b']
                        }
                        nhlboardrender.draw_outer_border(matrix, font, team_color)
                        nhlboardrender.draw_time_period_border(matrix, font, team_color)
                        
                        if (current_game_state == "Preview"):
                            print('should render')
                            nhlboardrender.draw_away_team_pre_game(matrix, font, color_white, game_data)
                            nhlboardrender.draw_home_team_pre_game(matrix, font, color_white, game_data)
                            # Must use threads for the matrix
                            scroll_thread = ScrollNextGameThread(matrix, font, color_white, team_color, game_data, break_scroll_thread)
                            scroll_thread.start()
                        elif(current_game_state == "Live" or current_game_state == "Final"):
                            nhlboardrender.draw_live_helper(matrix, font, color_white, game_data)
                            # Must use threads for the matrix
                            carousel_thread = CarouselThread(matrix, font, color_white, game_data, 1.8, break_carousel_thread)
                            carousel_thread.start()
                            pass

                # Update current board state for next iteration of loop
                # dont need this, setting in set_team_and_fetch_nhl_data
                current_board_state = shared_board_state.value
                print('board waiting for game data')
                game_data = rest_api_queue.get()
                # tell thread to stop because we have new data now
                with break_scroll_thread.get_lock():
                    break_scroll_thread.value = True
                    print('set break_scroll_thread to True')
                # do same again for carousel
                with break_carousel_thread.get_lock():
                    break_carousel_thread.value = True
                    print('set break_carousel_thread to True')
                print('end of loop')
            except Exception as e:
                print('e', e)
                #time.sleep(10)
                pass

