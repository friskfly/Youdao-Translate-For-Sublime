#coding:utf-8
import sublime, sublime_plugin
import urllib
import json
api="http://fanyi.youdao.com/openapi.do?keyfrom=friskfly&key=1410212834&type=data&doctype=json&version=1.1&q="
class YoudaoTranslateCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		selection = self.view.substr( self.view.sel()[0] ).encode('utf-8')
		url = api + urllib.quote(selection)
		try :
			data = json.loads(urllib.urlopen(url).read().decode('utf-8'))
			result = {
				'0': self.format(data),
				'20': "要翻译的文本过长",
				'30': "无法进行有效的翻译",
				'40': "不支持的语言类型",
				'50': "有道api接口出了点问题，请联系作者 weibo/friskfly"
			}[str(data['errorCode'])]
			self.createWindowWithText(result.decode('utf-8'))
		except Exception,ex:
			sublime.status_message("youdao translate connect error")

	def format(self,data):
		result = data['query'].encode('utf-8') +"\n\n最优结果："
		if 'translation' in data:
			for i in data['translation']:
				result += i.encode('utf-8') + ','
		result = result + "\n\n基本释义："
		if 'basic' in data:
			for i in data['basic']['explains']:
				result += i.encode('utf-8') + ','
		result = result + "\n\n相关释义：\n----------------------------------------------------------\n"
		if 'web' in data:
			for i in data['web']:
				result += i['key'].encode('utf-8') + "  "
				for y in i['value'] :
					result += y.encode('utf-8') + ','
				result +="\n"
		return result

	def createWindowWithText(self, textToDisplay):
		newView = self.view.window().new_file()
		edit = newView.begin_edit()
		newView.insert(edit, 0, textToDisplay)
		newView.end_edit(edit)
		newView.set_scratch(True)
		newView.set_read_only(True)
		newView.set_name("translate result")
		newView.set_syntax_file("Packages/JavaScript/JSON.tmLanguage")
		return newView.id()

