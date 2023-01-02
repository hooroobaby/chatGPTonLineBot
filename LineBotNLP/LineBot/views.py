from ast import IsNot
from cgitb import text
from cmath import isnan
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import openai

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
openai.api_key = settings.CHATGPT_KEY


# 製作chatGPT的回答
def create(prompt="開始", model="text-davinci-003",
           temperature=0, max_tokens=60, top_p=1.0,
           frequency_penalty=0.0, presence_penalty=0.0, stop=[]): 
  if stop==[]:
    response = openai.Completion.create(
      model=model,
      prompt=prompt,
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty
    )
  else:
    response = openai.Completion.create(
      model=model,
      prompt=prompt,
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty,
      stop=stop
    )
  print(response.choices[0].text)
  print(response)
  return response.choices[0].text;
  # chatGPT = response.choices[0].text
  # return chatGPT


# 情緒，要請使用者在後面加上，"情緒"二字
def emotion_long():
    prompt="我現在真的很不爽 貢丸湯沒有給我貢丸，我的情緒是："
    frequency_penalty=0.5
    create(prompt=prompt, frequency_penalty=frequency_penalty)

# 居子正負面情緒
def positive_or_negative():
    prompt="Decide whether a Tweet's sentiment is positive, neutral, or negative.\n\nTweet: \"這貢丸湯沒貢丸...\"\nSentiment:"
    frequency_penalty=0.5
    create(prompt=prompt,frequency_penalty=frequency_penalty)

# Grammar correction
# 請輸入幫我訂正文法，並在其後方輸入一段英文
def grammer_correction():
    prompt="幫我訂正文法：hihi, im an beauty"
    create(prompt=prompt)

def translate():
    # 翻譯Translate
    # 請輸入幫我翻譯成[任一種語言(如:中文、英文、法文...)]，並在其後方輸入一段句子
    prompt="幫我翻譯成英文：哈哈，好好笑"
    create(prompt=prompt)

def code_to_nlp():
    # 把python程式碼，轉成自然語言
    # 請直接輸入一段程式碼，請勿輸入其他會造成程式錯誤的句子，謝謝
    model="code-davinci-002"
    ###### 結尾要幫他們加上Explanation of what the code does\n\n#
    prompt="# Python 3 \ndef remove_common_prefix(x, prefix, ws_prefix): \n    x[\"completion\"] = x[\"completion\"].str[len(prefix) :] \n    if ws_prefix: \n        # keep the single whitespace as prefix \n        x[\"completion\"] = \" \" + x[\"completion\"] \nreturn x \n\n# Explanation of what the code does\n\n#"
    max_tokens=64
    create(model=model, prompt=prompt, max_tokens=max_tokens)

# 解釋程式碼
# 請輸入一段程式碼
def code_explain():
    model="code-davinci-002"
    prompt="class Log:\n    def __init__(self, path):\n        dirname = os.path.dirname(path)\n        os.makedirs(dirname, exist_ok=True)\n        f = open(path, \"a+\")\n\n        # Check that the file is newline-terminated\n        size = os.path.getsize(path)\n        if size > 0:\n            f.seek(size - 1)\n            end = f.read(1)\n            if end != \"\\n\":\n                f.write(\"\\n\")\n        self.f = f\n        self.path = path\n\n    def log(self, event):\n        event[\"_event_id\"] = str(uuid.uuid4())\n        json.dump(event, self.f)\n        self.f.write(\"\\n\")\n\n    def state(self):\n        state = {\"complete\": set(), \"last\": None}\n        for line in open(self.path):\n            event = json.loads(line)\n            if event[\"type\"] == \"submit\" and event[\"success\"]:\n                state[\"complete\"].add(event[\"id\"])\n                state[\"last\"] = event\n        return state\n\n\"\"\"\nHere's what the above class is doing:\n1."
    max_tokens=64
    stop=["\"\"\""]
    create(model=model, prompt=prompt, max_tokens=max_tokens, stop=stop)

# 會議紀錄的summarize
def summarize_meeting():
    prompt="Convert my short hand into a first-hand account of the meeting:\n\nTom: Profits up 50%\nJane: New servers are online\nKjel: Need more time to fix software\nJane: Happy to help\nParkman: Beta testing almost done"
    max_tokens=64
    create(prompt=prompt, max_tokens=max_tokens)

# 摘要
#https://beta.openai.com/examples
# 尾部加"Tl;dr:"
def TLDR():
    prompt="A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr:"
    temperature=0.7
    presence_penalty=1
    create(prompt=prompt, temperature=temperature, presence_penalty=presence_penalty)

# Friend chat
def chat_friend(prompt):
    temperature=0.5
    frequency_penalty=0.5
    stop=["You:"]
    max_tokens=300
    return create(prompt=prompt, temperature=temperature, max_tokens=max_tokens, frequency_penalty=frequency_penalty, stop=stop)

def chat_AI_assistant(prompt):
    # 你的AI助理
    # Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.
    # prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: 我減肥失敗，怎麼辦，我很努力了，還是瘦不下來，你可以安慰我嗎？\nAI:"
    temperature=0.9
    max_tokens=300
    presence_penalty=0.6
    stop=[" Human:", " AI:"]
    return create(prompt=prompt, temperature=temperature, max_tokens=max_tokens, presence_penalty=presence_penalty, stop=stop)

# 嘲諷聊天機器人 -> Marv the sarcastic chat bot
# How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\nYou: What time is it?
def chat_sarcastic(prompt):
    # prompt="Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: 我的報告做不出來了 怎麼辦？\nMarv:"
    temperature=0.5
    top_p=0.3
    frequency_penalty=0.5
    max_tokens=300
    return create(prompt=prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty)


# 宣告變數
history="" 
mode=""
preMode = mode

# pip install openai
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
    
        # 設定為全域變數，防止呼叫一次callback就忘記
        global history
        global mode
        global preMode
        
        for event in events:
            if isinstance(event , MessageEvent):
                print(event)
                print("history"+history) # 印出測試用

                # 如果使用者主動更換模式的話
                if event.message.text=="answers questions with sarcastic responses:":
                    mode = 'chat_sarcastic'
                    if mode != preMode:
                        history=""
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已為您更換成"+mode+"模式")
                    )
                    break;
                elif event.message.text=="conversation with an AI assistant.":
                    mode = 'chat_AI_assistant'
                    if mode != preMode:
                        history=""
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已為您更換成"+mode+"模式")
                    )
                    break;
                elif event.message.text == "Friend chat":
                    mode = 'chat_friend'
                    if mode != preMode:
                        history=""
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已為您更換成"+mode+"模式")
                    )
                    break;

                match(mode): # 確認現在的mode，使哪一種機器人
                    case 'chat_sarcastic':
                        if history =="":
                            prompt = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: "+event.message.text+"\n\nMarv: "
                            history = prompt
                            text_return = chat_sarcastic(prompt)

                        else:
                            prompt = history+"\n\nYou: "+event.message.text+"\n\nMarv: "
                            text_return = chat_sarcastic(prompt)
                            history = history+text_return+"\n\nYou: "+event.message.text+"\n\nMarv: "
                        
                        line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=text_return)
                        )
                        break
                    # ------------------------AI assistant
                    case 'chat_AI_assistant':
                        if history =="":
                            prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: "+event.message.text+"\nAI: "
                            # text_return = chat_AI_assistant(prompt)+"\n\n我現在在這"
                            history = prompt
                            text_return = chat_AI_assistant(prompt)

                        else:
                            prompt = history+"\n\nYou: "+event.message.text+"\n\AI: "
                            # text_return = chat_AI_assistant(prompt)+"\n\n我的history="+history
                            text_return = chat_AI_assistant(prompt)
                            history = history+text_return+"\n\nHuman: "+event.message.text+"\n\nAI: "

                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=text_return)
                        )
                        break
                    # --------------------Friend chat
                    case 'chat_friend':
                        if history =="":
                            prompt = "You: "+event.message.text+"\nFriend: "
                            history = prompt
                            text_return = chat_friend(prompt)

                        else:
                            prompt = history+"\n\nYou: "+event.message.text+"\nFriend: "
                            text_return = chat_friend(prompt)
                            history = history+text_return+"\nYou: "+event.message.text+"\n\nFriend: "

                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=text_return)
                        )
                        break
                
                # 最後將premode改為現在這個mode，讓下一次確認是否改變
                preMode = mode

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
