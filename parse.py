from gne import GeneralNewsExtractor
from fastapi import FastAPI, Body
from pydantic import BaseModel
import sys
import uvicorn

app = FastAPI(title='GNE网页信息提取接口', version='1.0.0')
extractor = GeneralNewsExtractor()


def parse_from_html(
        html: str,
        host: str,
        title_xpath: str,
        author_xpath: str,
        publish_time_xpath: str,
        body_xpath: str,
        noise_node_list: list,
        with_body_html: bool,
    ) -> dict:
    """根据 html 提取新闻内容"""
    global extractor
    try:
        result = extractor.extract(
            html=html,
            host=host,
            title_xpath=title_xpath,
            author_xpath=author_xpath,
            publish_time_xpath=publish_time_xpath,
            body_xpath=body_xpath,
            noise_node_list=noise_node_list,
            with_body_html=with_body_html
        )
    except Exception as e:
        raise Exception(f'Html parsing error, reason: {e}')
    return result


class SuccessfulTempItem(BaseModel):
    errCode: int = Body(0, description='错误状态码，值为0时表示请求成功')
    errMsg: str = Body(None, description='请求错误信息')
    result: dict = Body(None, description='请求结果')


class Item(BaseModel):
    html: str = Body(..., description='待解析的html文本')
    host: str = Body('', description='网站域名')
    title_xpath: str = Body('', description='标题xpath规则')
    author_xpath: str = Body('', description='作者xpath规则')
    publish_time_xpath: str = Body('', description='发布时间xpath规则')
    body_xpath: str = Body('', description='正文xpath规则')
    noise_node_list: list = Body(None, description='噪点xpath规则列表（提取器不会解析此列表内的xpath）')
    with_body_html: bool = Body(True, description='是否提取正文html')


@app.post('/gne/parse', response_model=SuccessfulTempItem, tags=['解析接口'])
async def parse(item: Item):
    """提取html中的信息"""
    if not item.html:
        return {'errCode:': 1, 'errMsg': '缺少html参数', 'result': None}
    try:
        html = item.html.encode('ISO-8859-1').decode()
    except (UnicodeEncodeError, UnicodeDecodeError):
        html = item.html
    try:
        result = parse_from_html(
            html,
            item.host,
            item.title_xpath,
            item.author_xpath,
            item.publish_time_xpath,
            item.body_xpath,
            item.noise_node_list,
            item.with_body_html,
        )
    except Exception as e:
        return {'errCode:': 1, 'errMsg': str(e), 'result': None}
    else:
        return {'errCode:': 0, 'errMsg': None, 'result': result}


if __name__ == '__main__':
    port = int(sys.argv[1])if len(sys.argv) > 1 else 8000
    uvicorn.run('parse:app', host='0.0.0.0', port=port, workers=4)
