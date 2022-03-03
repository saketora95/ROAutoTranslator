import datetime
import os
import translator

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

CURRENT_DATE = datetime.datetime.now()
CURRENT_DATE_STRING = datetime.datetime.strftime(CURRENT_DATE, DATE_FORMAT)

EXECUTE_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
LOG_PATH = EXECUTE_PATH + 'Log/'
COMPARE_LIST_PATH = EXECUTE_PATH + 'Compare List.txt'

# Check log exist
if os.path.isdir(LOG_PATH) == False:
    os.mkdir(LOG_PATH)

# Check compare list exist
compare_file_exsit = os.path.isfile(COMPARE_LIST_PATH)
if compare_file_exsit:
    print('存在 ' + COMPARE_LIST_PATH + ' 檔案。')

    main_win = translator.Translator(CURRENT_DATE_STRING, LOG_PATH, COMPARE_LIST_PATH)
    main_win.mainloop()

else:
    print('缺少 ' + COMPARE_LIST_PATH + ' 檔案，無法進行後續步驟。')