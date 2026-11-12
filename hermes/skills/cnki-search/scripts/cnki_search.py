#!/usr/bin/env python3
"""
CNKI搜索辅助脚本
用于解析知网搜索结果页面
"""

import re
import json
from typing import List, Dict, Optional

def parse_search_results(html_content: str) -> List[Dict]:
    """
    解析知网搜索结果页面
    
    Args:
        html_content: 页面HTML内容
        
    Returns:
        论文列表，每个论文包含标题、作者、期刊等信息
    """
    papers = []
    
    # 提取论文条目的正则表达式
    # 知网结果页面通常包含以下结构：
    # <tr>...<a class="fz14" href="...">标题</a>...<td>作者</td>...<td>期刊</td>...</tr>
    
    # 这里提供基础解析逻辑，实际使用时需要根据页面结构调整
    pattern = r'<a[^>]*class="fz14"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
    matches = re.findall(pattern, html_content)
    
    for href, title in matches:
        papers.append({
            'title': title.strip(),
            'url': href if href.startswith('http') else f'https://kns.cnki.net{href}',
            'authors': '',
            'journal': '',
            'year': '',
            'downloads': ''
        })
    
    return papers

def extract_paper_detail(html_content: str) -> Dict:
    """
    提取论文详情页信息
    
    Args:
        html_content: 详情页HTML内容
        
    Returns:
        论文详细信息字典
    """
    detail = {
        'title': '',
        'authors': [],
        'journal': '',
        'year': '',
        'volume': '',
        'issue': '',
        'pages': '',
        'doi': '',
        'abstract': '',
        'keywords': [],
        'fund': '',
        'download_pdf': '',
        'download_caj': ''
    }
    
    # 提取标题
    title_match = re.search(r'<h1[^>]*>([^<]*)</h1>', html_content)
    if title_match:
        detail['title'] = title_match.group(1).strip()
    
    # 提取作者
    author_pattern = r'<a[^>]*class="author"[^>]*>([^<]*)</a>'
    authors = re.findall(author_pattern, html_content)
    detail['authors'] = [a.strip() for a in authors]
    
    # 提取摘要
    abstract_match = re.search(r'<div[^>]*class="abstract"[^>]*>(.*?)</div>', html_content, re.DOTALL)
    if abstract_match:
        abstract = re.sub(r'<[^>]+>', '', abstract_match.group(1))
        detail['abstract'] = abstract.strip()
    
    # 提取关键词
    keyword_pattern = r'<a[^>]*class="keyword"[^>]*>([^<]*)</a>'
    keywords = re.findall(keyword_pattern, html_content)
    detail['keywords'] = [k.strip() for k in keywords]
    
    # 提取下载链接
    pdf_match = re.search(r'href="([^"]*\.pdf[^"]*)"', html_content)
    if pdf_match:
        detail['download_pdf'] = pdf_match.group(1)
    
    caj_match = re.search(r'href="([^"]*\.caj[^"]*)"', html_content)
    if caj_match:
        detail['download_caj'] = caj_match.group(1)
    
    return detail

def format_results(papers: List[Dict], output_format: str = 'text') -> str:
    """
    格式化搜索结果
    
    Args:
        papers: 论文列表
        output_format: 输出格式 ('text', 'json', 'csv')
        
    Returns:
        格式化后的字符串
    """
    if output_format == 'json':
        return json.dumps(papers, ensure_ascii=False, indent=2)
    
    elif output_format == 'csv':
        if not papers:
            return ''
        headers = papers[0].keys()
        lines = [','.join(headers)]
        for paper in papers:
            lines.append(','.join(str(paper.get(h, '')) for h in headers))
        return '\n'.join(lines)
    
    else:  # text format
        lines = []
        for i, paper in enumerate(papers, 1):
            lines.append(f"{i}. {paper.get('title', 'N/A')}")
            if paper.get('authors'):
                lines.append(f"   作者: {paper['authors']}")
            if paper.get('journal'):
                lines.append(f"   期刊: {paper['journal']}")
            if paper.get('year'):
                lines.append(f"   年份: {paper['year']}")
            lines.append('')
        return '\n'.join(lines)

if __name__ == '__main__':
    # 测试代码
    test_html = '''
    <html>
    <body>
    <a class="fz14" href="/kcms/detail/123">颈椎病MRI诊断研究</a>
    </body>
    </html>
    '''
    
    results = parse_search_results(test_html)
    print(format_results(results, 'text'))
