import time
import nhl_game_data as nhlgamedata

def get_time_since_game_ended(seconds):
    return time.time() - seconds

def set_team_and_fetch_nhl_data(shared_mem_team, rest_api_queue, shared_board_state, shared_board_brightness, shared_sleep_timer):
    # At runtime set the shared_mem_team value (the settings team id)
    # to the current team id 
    current_team_id = shared_mem_team.value
    # do the same for the board state
    # Update current board state for next iteration of loop
    current_board_state = shared_board_state.value
    # do this for the birghtness too
    current_brightness = shared_board_brightness.value
    # game state get set later by fetch and parse
    game_state = None
    game_end_time = None
    
    # Always get pregame data at boot
    pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
    parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)
    
    # Get the tiem in seconds when the board turned
    boot_time = time.time()

    # Never break from outer loop
    while True:
        # Basically the point of all this code here is 
        # so we dont keep downloading the pre game data is the game is live
        
        # User changed to another team, start the process over
        if current_team_id != shared_mem_team.value:
            # get pre game data
            pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
            parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)

        ''' If the game has been over for 15 minutes from now
            and the next game doesn't for more than 15 minutes from now
            shared_sleep_timer == 0 means don't turn off ever
        '''
        # Is the sleep timer set
        if shared_sleep_timer.value != 0:
            print('sleep timer set')
            # did it just turn on, boot_time or did the team change            
            if time.time() > (boot_time + (shared_sleep_timer.value * 60)) or current_team_id != shared_mem_team.value:
                print('time since boot greater than boot time plus sleep')
                # did the board state change from 0 to 1
                if current_board_state == 0 and shared_board_state.value == 1:
                    print('current board state 0 and shared_board_state 1')
                    # game is not over
                    if game_end_time is not None:
                        # its been the sleep timer value since the game ended
                        if get_time_since_game_ended(game_end_time) > shared_sleep_timer.value * 60:
                            with shared_board_state.get_lock():
                                shared_board_state.value = 0

                    game_start_time = time.mktime(parsed_pre_game_data['gameStartDateTime'].timetuple())
                    time_until_next_game_starts = game_start_time - time.time()
                    # the game won't start for more than the sleep timers value
                    if time_until_next_game_starts > shared_sleep_timer.value * 60:
                        with shared_board_state.get_lock():
                            shared_board_state.value = 0


        # Store what the current team is for comparison
        current_team_id = shared_mem_team.value
        # do the same for the board state
        current_board_state = shared_board_state.value
        # do the same for the brightness
        current_brightness = shared_board_brightness.value

        # What happens here is if the game has been over for more than 15 minutes,
        # get the next game data, which will be in state "Preview" so if the game was 
        # showing live data this will make it show preview data for the next game
        if game_end_time is not None:
            if get_time_since_game_ended(game_end_time) > 900:
                # get pre game data
                pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
                parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)

        

        # if there is not a game coming anytime soon,
        # we want to slee for a longer time
        seconds_to_sleep = 10
        if parsed_pre_game_data['gameId'] is None:
            seconds_to_sleep = 86400

        # The final gameState data will only be donwloaded once
        # Also make sure there is a next gameId
        # If game is Live or Preview
        #if (game_state != "Final" or parsed_pre_game_data['gameId'] is not None):
        if (parsed_pre_game_data['gameId'] is not None):
            # Download live data
            live_game_data = nhlgamedata.fetch_live_game_data(parsed_pre_game_data['gameId'])
            parsed_live_game_data = nhlgamedata.get_parsed_live_game_data(live_game_data)

            ''' We need abbrevations from live data for our pre game data
            '''
            parsed_pre_game_data['awayTeam'] = parsed_live_game_data['awayTeam']
            parsed_pre_game_data['homeTeam'] = parsed_live_game_data['homeTeam']

            ''' We need to add current_team_id to pre_game and live_game
                data so that our color can be chosen based on what the user
                chose for which team, that is which team number the rest api received
            '''
            parsed_pre_game_data['currentTeamId'] = current_team_id
            parsed_live_game_data['currentTeamId'] = current_team_id

            ''' Check if the game is live or not
                Depending on the game state, tell the board to disply different things
            '''
            game_state = parsed_live_game_data['gameState']
            print(game_state)
            if (game_state == "Preview"):
                # now both pre and live have gameState
                parsed_pre_game_data['gameState'] = "Preview"
                rest_api_queue.put(parsed_pre_game_data)
                seconds_to_sleep = 15
                print('is preview')
            elif (game_state == "Live"):
                rest_api_queue.put(parsed_live_game_data)
                print('is live')
            # would never hit this becuase game_state != "Final"
            elif (game_state == "Final"):
                rest_api_queue.put(parsed_live_game_data)
                print('is final')
            else:
                print('not any of those')
            # We will modifly the Previe and FInal if statemtns based on this extra info
            #elif (if the game has ended more than 15 minutes ago shut off the board)
            #elif (if the game is going to start in 15 minutes or less then turn on the board)
        else:
            if 'gameEndDateTime' in parsed_live_game_data:
                game_end_time = time.mktime(parsed_live_game_data['gameEndDateTime'].timetuple())

        # 10 second sleep function
        timeout = time.time() + seconds_to_sleep
        while True:
            # While we are sleeping check ever 0.25 seconds 
            # if the API updated the team id
            if current_team_id != shared_mem_team.value:
                break
            elif current_board_state != shared_board_state.value:
                break
            elif current_brightness != shared_board_brightness.value:
                break
            else:
                # if it's been 10 seconds break
                if time.time() > timeout:
                    break
                else:
                    time.sleep(0.1)
