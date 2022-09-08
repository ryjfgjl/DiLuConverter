import webbrowser

class Setting:

    def __init__(self):
        self.event = None
        self.values = {}
        self.window = None
        self.show_window = None

    def main(self):
        if self.event in ['English', '中文']:
            # change language
            self.values['language'] = self.event
            self.window.close()
            self.window = self.show_window(self.values)

        elif self.event in ['MySQL', 'Oracle', 'SQL Server', 'Hive']:
            # change database type
            self.values['dbtype'] = self.event
            self.window['dbtype'].update(self.event)
        
        elif self.event in ['Directory', 'Files', '目录', '文件']:
            # change data source
            if self.event in ['Directory', '目录']:
                source = 'D'
            else:
                source = 'F'
            self.values['source'] = source
            self.window.close()
            self.window = self.show_window(self.values)
        elif self.event in ['Document', '在线文档']:
            if self.event == 'Document':
                webbrowser.open('https://github.com/ryjfgjl/ExcelToDatabase/blob/master/README.md')
            else:
                webbrowser.open('https://blog.csdn.net/qq_37955852/article/details/122488507')

        elif self.event == 'save_config':
            if self.values['current_config']:
                with open(f"saved_configuration/{self.values['current_config']}.ini", 'w', encoding='utf8') as fw:
                    fw.truncate()
            self.window.close()
            self.window = self.show_window(self.values)
        elif self.event == 'load_config':
            if self.values['saved_config']:
                self.values['current_config'] = self.values['saved_config']

        return self.window

