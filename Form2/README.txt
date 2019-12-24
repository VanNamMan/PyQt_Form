pyuic5 -x UI/main.ui -o header/mainUi.py
pyuic5 -x UI/parameter.ui -o header/parameterUi.py
pyuic5 -x UI/result.ui -o header/resultUi.py
pyuic5 -x UI/treeShape.ui -o header/treeShapeUi.py

pyrcc5 -o libs_/resources.py resources.qrc
