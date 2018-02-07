"""
    - get live data
    - parse currentPeriod
    - parse currentPeriodOrdinal
    - parse currentPeriodTimeRemaining
    - parse intermissionTimeRemaining

    - if abstractGameState == Preview (before the game starts)
        - set time to 00:00
        - set period to PRE
    - else if abstractGameState == Final (is the game over)
        - set time to 00:00
         - set period to END
    - else if (abstractGameState == Live) && (intermissionTimeRemaining != 0) (intermission)
        - set time to 00:00
        - set period to InT
    - else if (abstractGameState == Live) && (intermissionTimeRemaining == 0) (game is live)
        - set period to currentPeriodOrdinal
        - get all stoppage events
        - stoppage.count > 0
            - find the last stoppage
            - is stoppage in the same period
                - if currentPeriodTimeRemaining == periodTimeRemaining (+/- 1 second (i saw be periodTimeRemaining 2 while currentPeriodTimeRemaining was 1))
                    - set time to periodTimeRemaining
                - else
                    - start counter at currentPeriodTimeRemaining
        - else 
            - start counter at currentPeriodTimeRemaining
    
"""