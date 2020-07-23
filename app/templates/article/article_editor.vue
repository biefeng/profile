{%raw%}
<template id="article-editor">

    <div id="editor" v-loading="loadingId > 0">
        <div style="padding: 15px 0; ">
            <el-input style="width: 300px;" v-model="article.title" placeholder="标题"></el-input>
            <el-select v-model="article.articleType_id" placeholder="类型">
                <el-option
                        v-for="item in articleTypes"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id">
                </el-option>
            </el-select>
            <el-select v-model="article.private" placeholder="私密/公开">
                <el-option
                        v-for="item in displayOptions"
                        :key="item.value"
                        :label="item.name"
                        :value="item.value">
                </el-option>
            </el-select>

            <el-input style="margin-top: 10px" v-model="article.summary" placeholder="简描述"></el-input>
        </div>
        <mavon-editor class="mavonEditor"
                      :subfield="subfield"
                      :code-style="code_style"
                      v-on:save="saveArticle(context)"
                      :external-link="externalLink"
                      v-model="article.content_md"></mavon-editor>
        <div style="margin-top: 10px;text-align: right">
            <el-button type="primary" @click="clearContent">清空</el-button>
            <el-button type="success" @click="saveArticle">保存</el-button>
        </div>
    </div>
</template>
{%endraw%}
<!--<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js"></script>-->
<script src="https://cdn.jsdelivr.net/npm/mavon-editor@2.9.0/dist/mavon-editor.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mavon-editor@2.9.0/dist/css/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.min.css">
<script>

    Vue.use(MavonEditor)

    Vue.component("main-content", {
        template: "#article-editor",
        data() {
            return {
                context: " ", //输入的数据
                ishljs: true,
                toolbarsFlag: true,
                toolbars: {
                    bold: true, // 粗体
                    italic: true, // 斜体
                    header: true, // 标题
                    underline: true, // 下划线
                    mark: true, // 标记
                    superscript: true, // 上角标
                    quote: true, // 引用
                    ol: true, // 有序列表
                    link: true, // 链接
                    imagelink: true, // 图片链接
                    help: true, // 帮助
                    code: true, // code
                    subfield: true, // 是否需要分栏
                    fullscreen: true, // 全屏编辑
                    readmodel: true, // 沉浸式阅读
                    /* 1.3.5 */
                    undo: true, // 上一步
                    trash: true, // 清空
                    save: true, // 保存（触发events中的save事件）
                    /* 1.4.2 */
                    navigation: true // 导航目录
                },
                subfield: true,
                code_style: "atom-one-dark",
                externalLink: {
                    markdown_css: function () {
                        // 这是你的markdown css文件路径
                        return "";
                    },
                    hljs_js: function () {
                        // 这是你的hljs文件路径
                        return "https://cdn.jsdelivr.net/npm/highlight.js@10.1.1/lib/index.min.js";
                    },
                    hljs_css: function (css) {
                        // 这是你的代码高亮配色文件路径
                        return "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css";
                    },
                    hljs_lang: function (lang) {
                        // 这是你的代码高亮语言解析路径
                        return "";
                    },
                    katex_js: function () {
                        return "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js"
                    }
                },
                article: {
                    id: '{{id}}',
                    title: '',
                    content_md: '',
                    articleType_id: undefined,
                    content: '',
                    private: undefined,
                    summary: ''
                },
                articleTypes: [],

                displayOptions: [],
                loadingId: '{{id}}',  //用来控制是否做loading
            }
        },
        computed: {},
        updated() {

        },
        created() {
            if (this.article.id && this.article.id > 0) {
                this.loadArticle()
            }
            this.loadOptions()

        },
        methods: {
            saveArticle(content) {
                if (!this.article.title || !this.article.content_md) {
                    this.$message.error("标题和内容不能为空")
                    return
                }
                let markdownIt = MavonEditor.markdownIt;
                this.article.content = markdownIt.render(this.article.content_md)
                this.$http.post("/article/save", this.article).then(res => {
                    console.log(res)
                }).catch(e => {
                    console.log(e)
                })
            },
            clearContent() {
                this.article.content_md = ''
            },
            loadArticle() {
                this.$http.get("/article/get", {
                    params: {id: this.article.id}
                }).then(res => {
                    Object.assign(this.article, res.data)
                    console.log(this.article)
                    this.loadingId = 0
                }).catch(e => {
                    this.loadingId = 0
                })
            },
            loadOptions() {
                this.$http.get("/article_type/list").then(res => {
                    this.articleTypes = res.data
                })
                this.$http.post("/enum/", ["DISPLAY_TYPE"]).then(res => {
                    let data = res.data;
                    if (data) {
                        this.displayOptions = data['DISPLAY_TYPE']
                    }
                })
            }
        }
    });
</script>
<style>
    .mavonEditor h1 {
        font-size: 2em;
    }

</style>

