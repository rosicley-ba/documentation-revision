from bs4 import BeautifulSoup


def get_the_clean_file(file_name: str):
    new_html: str = ""
    with open(file_name, "r", encoding="UTF8") as our_html:
        file_start = False

        for line in our_html:
            if '<div id="main-content" class="wiki-content group">' in line:
                file_start = True
            elif file_start:
                if "                    </div>" in line:
                    break
                new_html += line
    return new_html


def get_replaced_fields(new_html: str):
    modified_html = new_html
    replace = {}
    replace["<code>"] = '<span class="code">'
    replace["</code>"] = "</span>"
    replace[
        '<div class="code panel pdl" style="border-width: 1px;"><div class="codeContent panelContent pdl">\n<pre class="syntaxhighlighter-pre" data-syntaxhighlighter-params="brush: bash; gutter: false; theme: Confluence" data-theme="Confluence">'
    ] = '<ac:structured-macro ac:macro-id="" ac:name="code" ac:schema-version="1">\n <ac:parameter ac:name="language">powershell</ac:parameter>\n <ac:parameter ac:name="linenumbers">true</ac:parameter>\n <ac:plain-text-body><![CDATA['
    replace[
        "</pre>\n</div></div>"
    ] = "]]>\n</ac:plain-text-body>\n</ac:structured-macro>"
    replace[
        '<div class="code panel pdl" style="border-width: 1px;"><div class="codeContent panelContent pdl">\n<pre class="syntaxhighlighter-pre" data-syntaxhighlighter-params="brush: powershell; gutter: false; theme: Confluence" data-theme="Confluence">'
    ] = '<ac:structured-macro ac:macro-id="" ac:name="code" ac:schema-version="1">\n <ac:parameter ac:name="language">powershell</ac:parameter>\n <ac:parameter ac:name="linenumbers">true</ac:parameter>\n <ac:plain-text-body><![CDATA['
    replace[
        '<div class="code panel pdl" style="border-width: 1px;"><div class="codeContent panelContent pdl">\n<pre class="syntaxhighlighter-pre" data-syntaxhighlighter-params="brush: plan; gutter: false; theme: Confluence" data-theme="Confluence">'
    ] = '<ac:structured-macro ac:macro-id="" ac:name="code" ac:schema-version="1">\n <ac:parameter ac:name="language">powershell</ac:parameter>\n <ac:parameter ac:name="linenumbers">true</ac:parameter>\n <ac:plain-text-body><![CDATA['
    replace[
        '<div class="code panel pdl" style="border-width: 1px;"><div class="codeContent panelContent pdl">\n<pre class="syntaxhighlighter-pre" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence">'
    ] = '<ac:structured-macro ac:macro-id="" ac:name="code" ac:schema-version="1">\n <ac:parameter ac:name="language">yaml</ac:parameter>\n <ac:parameter ac:name="linenumbers">true</ac:parameter>\n <ac:plain-text-body><![CDATA['
    replace[
        '<div class="confluence-information-macro confluence-information-macro-information"><span class="aui-icon aui-icon-small aui-iconfont-info confluence-information-macro-icon"></span><div class="confluence-information-macro-body"><p>'
    ] = '<ac:structured-macro ac:macro-id="" ac:name="info" ac:schema-version="1">\n <ac:rich-text-body>'
    replace["</p></div></div>"] = "</ac:rich-text-body>\n</ac:structured-macro>"
    replace[
        "</p></li></ul></div></div>"
    ] = "</p></li></ul></ac:rich-text-body>\n</ac:structured-macro>"
    replace["<ul>"] = '<ul class="ak-ul">'

    for old, new in replace.items():
        modified_html = modified_html.replace(old, new)

    return modified_html


def create_modified_html(file_name: str, file_name_to_save: str):
    modified_html = get_the_clean_file(file_name)
    modified_html = get_replaced_fields(modified_html)
    soup = BeautifulSoup(modified_html, "html.parser")
    tags_to_modify = soup.find_all("ac:structured-macro")
    replace = {}
    for tag in tags_to_modify:
        for cont in tag.contents:
            name = cont.name
            if "ac:plain-text-body" == name:
                replace[cont.text] = (
                    cont.text.replace("&#39;", "'")
                    .replace("&lt;", "<")
                    .replace("&gt;", ">")
                )

    for old, new in replace.items():
        old_parts = old.split("\n")
        new_parts = new.split("\n")
        for old_part, new_part in zip(old_parts, new_parts):
            modified_html = modified_html.replace(old_part, new_part)

    # sou = soup.decode('soup')
    pretty_HTML = soup.prettify()
    with open(file_name_to_save, "w", encoding="UTF8") as new_file:
        new_file.write(modified_html.strip())


create_modified_html("original.html", "General Ansible Troubleshooting.html")

