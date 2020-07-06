{%raw%}
<template id="article-detail">
    <div class="article-detail-container">
        <div style="width: 100%;border:1px dashed red;">
            {{message}}
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
                content: ''
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
                    } else {
                        this.content = ""
                    }
                })
            }
        }
    });
</script>
<style>
.article-detail-container{
    text-align: left;
    background-color: #f0f0f0;
    padding: 15px;
}
</style>

