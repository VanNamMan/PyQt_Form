pyuic5 -x UI/main.ui -o header/mainUi.py
pyuic5 -x UI/parameter.ui -o header/parameterUi.py
pyuic5 -x UI/result.ui -o header/resultUi.py

pyrcc5 -o libs/resources.py resources.qrc
