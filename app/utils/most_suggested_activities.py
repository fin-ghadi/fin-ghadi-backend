

async def most_suggested_activities(activities , user , weather ,timestamp) :
    pass

"""

    this function take activities in argument with this properties
                            activities
                            {id
                            name: str
                            type: str
                            rating: Optional[float] = None   
                            distance: Optional[float] = None   
                            opening_hours: Optional[str] = None  
                            
                            userm{ gender 
                            age }
                            weather
                           { main 
                            description 
                            temperature
                            wind_speed
                            hunidity}
                            
                            timestamp
                            
        then its should using the propmt engeneer to filter the activitie and return just the most 13 recomended nearby activities 
        depending on weather weather and depend on the user.gender user.age and the timestamp becuz each activiti have opening_hours 
        also the recomendation should consider that the activitie should be entertainment of touristique of hangout so you should eliminate all the 
        other types of activities  
        and also for each recomended activity its should Generate a detailled construction that contain advises and wthat you should take with you 
        and also a detailed description for the activity 
        the output should be list of  objects of the 13 recomended activities the object should be like this 
        [
            {
                id
                constructions 
                description 
            }
        ]
        
     
"""