import os
import ocr

# 遇到新的再加
assignArray = ['int32_t', 'int64_t', 'BOOL']
copyArray = ['NSString *', 'NSArray *']

propertyMap = {
    'int32' : 'int32_t',
    'int64' : 'int64_t',
    'string' : 'NSString *',
    'bool' : 'BOOL'
}

def objectivecProperty(propertyName, typeName):
    result = '@property (nonatomic, '
    ocType = ''

    if 'List' in typeName:
        ocType = 'NSArray *'
    else:
        ocType = propertyMap[typeName]

    if ocType in assignArray:
        result += 'assign'
    elif ocType in copyArray:
        result += 'copy'
    else:
        result += 'strong'

    if 'List' in typeName:
        ocType += typeName.replace('List', '');

    result = result + ') '+ocType+' '+propertyName+';'
    return result



if __name__ == '__main__':
    p = os.popen('pip3 show baidu-aip')
    text = p.read()
    p.close()
    if 'Name: baidu-aip' not in text:
        p = os.popen('pip3 install baidu-aip')
        text = p.read()
        p.close()
        if text.isspace():
            print('install baidu-aip error')
            os._exit()

    imagePath = './screenshotImage.png'
    p = os.popen('screencapture -i '+imagePath)
    p.read()

    orcResult = ocr.startOcr().strip()
    textArray = orcResult.split(' ')
    objectivecResult = ''
    for i in range(len(textArray)):
        if i%2 != 0:
            propertyName = textArray[i-1]
            typeName = textArray[i]
            objectivecResult += objectivecProperty(propertyName, typeName)
            objectivecResult += '\n'
    os.system("echo '%s' | pbcopy" % objectivecResult)