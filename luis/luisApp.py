from botbuilder.core import TurnContext,ActivityHandler
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer
from botbuilder.ai.luis.luis_util import LuisUtil
import json
#from weather.weatherApp import WeatherInformation
from config.config_reader import ConfigReader
from logger.logger import Log


d = {"pay":"you need to pay 50k also you need to look in to potel"}

class LuisConnect(ActivityHandler):
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.luis_app_id=self.configuration['LUIS_APP_ID']
        self.luis_endpoint_key = self.configuration['LUIS_ENDPOINT_KEY']
        self.luis_endpoint = self.configuration['LUIS_ENDPOINT']
        self.luis_app = LuisApplication(self.luis_app_id,self.luis_endpoint_key,self.luis_endpoint)
        self.luis_options = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.luis_recognizer = LuisRecognizer(application=self.luis_app,prediction_options=self.luis_options,include_api_results=True)
        self.luis_util = LuisUtil()
        self.log=Log()
 

    async def on_message_activity(self,turn_context:TurnContext):
        #weather_info=WeatherInformation()
        luis_result = await self.luis_recognizer.recognize(turn_context)
        result = luis_result.properties["luisResult"]
        out = self.luis_util.luis_result_as_dict(result)
        print(out)
        weather = out['topScoringIntent']['intent']
        #weather = d[weather]
        #json_str = json.loads((str("hello")).replace("'", "\""))
        #weather=weather_info.get_weather_info(json_str.get('entity'))
        #weather = "i dont have anaswer"
        self.log.write_log(sessionID='session1',log_message="Bot Says: "+str(weather))
        await turn_context.send_activity(f"{weather}")
