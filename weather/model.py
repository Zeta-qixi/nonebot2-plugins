from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime
import base64
from io import BytesIO

class Weather:
    def __init__(self, params):
        self.temp = int(params['temp'])
        self.location = params['location']
        self.feelsLike = int(params['feelsLike'])
        self.text = params['text']                                 
        self.humidity = int(params['humidity']) 
        self.datetime = datetime.fromisoformat(params['obsTime'])
        self.icon =  chr(61597 + int(params['icon'])) 
        
    def __str__(self):
        return f"天气: {self.text}\n温度: {self.temp}°C\n湿度: {self.humidity}%"
     

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

class WeatherCardGenerator:
    def __init__(
        self,
        card_width=250,
        font_dir=Path('data/font'),
    ):
        self.card_width = card_width
        self.card_height = int(card_width * 1.4)
    
        default_font = 'sakura.ttf'

        self.font =  {
            'city': font_dir / default_font,
            'datetime': font_dir / default_font,
            'temperature': font_dir / 'YurukaFangTang.ttf',
            'text': font_dir / 'YurukaFangTang.ttf',
            'icon': font_dir / 'qweather-icons.ttf',
            'info': font_dir / default_font,
        }
        
        self.colors =  {
            'background': '#FFFFFF',
            'city': '#2D4059',
            'datetime': '#7D7D7D',
        }

        self.font_sizes = {
            'city': 32,
            'datetime': 20,
            'temperature': 40,
            'text': 40,
            'info': 24,
            'icon': 50
        }
    

    def _temperature_color(self, temp, min_temp=-30, max_temp = 45):
        """温度映射到颜色"""
        norm = plt.Normalize(vmin=min_temp, vmax=max_temp)
        colormap = plt.get_cmap('coolwarm')
        color = mcolors.to_hex(colormap(norm(int(temp))))
        return color

    def _create_card(self):
                
        img = Image.new('RGB', (self.card_width, self.card_height), self.colors['background'])        
        img = img.convert("RGBA")
        mask = Image.new('L', img.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([(0,0), img.size], radius=30, fill=255)
        img.putalpha(mask)
        return img
    
    def generate_card(self, weather_data: Weather, return_bytes=False) -> BytesIO:
        
        padding = 25
        self.layout = {
            'city_pos': (padding, padding-5),
            'datetime_pos': (padding, padding + 45),
            
            'icon_pos': (self.card_width // 2 - 15, self.card_height//3),
            
            'temp_pos': (padding, self.card_height//3 ),
            
            'text_pos': (padding, self.card_height//2 + padding),
            
            'feels_like_pos': (padding, self.card_height - padding - 65),
            'humidity_pos': (padding, self.card_height - padding - 25)
        }

        img = self._create_card()

        draw = ImageDraw.Draw(img)
        
        self._draw_text(draw, self.layout['city_pos'], weather_data.location, 
                        'city', self.colors['city'])
        
        # 时间
        self._draw_text(draw, self.layout['datetime_pos'], weather_data.datetime.strftime('%m-%d %H:%M'), 
                        'datetime', self.colors['datetime'])
        
   
        # 温度
        self._draw_text(draw, self.layout['temp_pos'], 
                        f"{weather_data.temp}°", 'temperature', self._temperature_color(weather_data.temp))
        
        # 气象
        self._draw_text(draw, self.layout['text_pos'], 
                        weather_data.text, 'text', self._temperature_color(weather_data.temp+10))
        
        #图标
        self._draw_text(draw, self.layout['icon_pos'], 
                        weather_data.icon, 'icon', self._temperature_color(weather_data.temp))
        
        # 体感
        self._draw_text(draw, self.layout['feels_like_pos'], 
                        f"体感温度: {weather_data.feelsLike}°C", 'info', self._temperature_color(weather_data.feelsLike))
        
        # 湿度
        self._draw_text(draw, self.layout['humidity_pos'], 
                        f"湿度: {weather_data.humidity}%", 'info', self._temperature_color(weather_data.feelsLike))

       
        buffered = BytesIO()
        img.save(buffered, format="PNG")  
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def _draw_text(self, draw, position, text, font_type, color):
        """通用文字绘制方法"""
        font = ImageFont.truetype(str(self.font[font_type]), self.font_sizes[font_type])
        draw.text(position, text, font=font, fill=color)






generator = WeatherCardGenerator()