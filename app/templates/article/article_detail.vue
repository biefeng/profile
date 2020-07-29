<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.min.css">
{%raw%}
<template id="article-detail">
    <div class="article-detail-container">
        <div class="article-detail-wrapper markdown-body" style="">
            <div v-html="content">

            </div>
        </div>
    </div>
</template>
{%endraw%}

<script>
    Vue.component("main-content", {
        template: "#article-detail",
        data() {
            return {
                message: "The is a sample component",
                id: '{{id}}',
                content: '',
                title: ''
            }
        },
        created() {
            this.loadArticle()

        },
        methods: {
            loadArticle() {
                this.$http.get("/article/get", {
                    params: {id: this.id}
                }).then(res => {
                    if (res.data && res.data.content) {
                        this.content = res.data.content
                        this.title = res.data.title
                    } else {
                        this.content = ""
                        this.title = 'Not Found'
                    }
                    document.title = this.title
                })
            }
        }
    });
</script>
<style>
    .article-detail-container {
        text-align: left;
        background-color: #f0f0f0ba;
        min-height: 100%;
    }

    .article-detail-wrapper {
        padding: 20px;
    }

</style>

