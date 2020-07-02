{% raw %}
<template id="article_list">

    <div class="article-list_container" v-loading="loading">
        <div class="article-list_item" v-for="article in articles">
            <div>
                <h3>
                    <a>{{article.title}}</a>
                </h3>
            </div>
            <div style="margin-bottom: 10px;">
                <div style="display: inline-block;">
                    <span class="colorful-label primary">
                        {{article.create_time}}
                    </span>
                    <span class="colorful-label warn">
                        {{article.source}}
                    </span>
                    <span class="colorful-label info">
                        未分类
                    </span>
                </div>
                <div style="float: right;display: inline-block;">
                    <span class="colorful-label success">
                        浏览数{{article.num_of_view}}
                    </span>
                    <span class="colorful-label warn">
                        评论189
                    </span>
                </div>
            </div>
            <div style="margin-bottom: 20px;">
                {{ article.summary}}
            </div>
        </div>
    </div>
</template>

{% endraw %}
<script>
    Vue.component("main-content", {
        template: "#article_list",
        data() {
            return {
                pageSize: 20,
                total: 0,
                articles: [],
                loading: false,
            }
        },
        created() {
            this.list(1)
        },
        methods: {
            list(pageNum, params) {
                this.loading = true
                let assign = Object.assign({pageNumber: pageNum, pageSize: this.pageSize}, params, this.query);
                if (pageNum != undefined) {
                    this.currentPage = pageNum
                }
                this.$http.get("/article/list-data", {
                    params: assign
                }).then(res => {
                    this.articles = res.data.list
                    this.total = res.data.total
                    this.loading = false
                }).catch(e => {
                    console.log(e)
                    this.loading = false
                })
            }
        }
    });
</script>
<style>
    .article-list_container {
        padding: 15px;
    }

    .article-list_item {
        margin: 0px 0px 15px 0px;;
        height: auto;
        padding: 15px;
        background-color: white;
        box-shadow: 0px 0px 3px gray;
    }
</style>

