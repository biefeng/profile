{% raw %}
<template id="article_list">

    <div class="article-list_wrapper">
        <div class="article-list_container" v-loading="loading">
            <a class="article-list_item-container" v-for="article in articles"
               :href="'/article/detail-view/'+article.id">
                <div class="article-list_item">
                    <div class="article-title">{{article.title}}</div>
                    <div class="info-label">
                        <div class="label-wrapper">
                            <span class="colorful-label primary">{{article.create_time}}</span>
                        </div>
                        <div class="label-wrapper">
                            <span class="colorful-label warn">{{article.source}}</span>
                        </div>
                        <div class="label-wrapper">
                            <span class="colorful-label info">未分类</span>
                        </div>
                        <div class="label-wrapper">
                            <span class="colorful-label hot">浏览数{{article.num_of_view}}</span>
                        </div>
                        <div class="label-wrapper">
                            <span class="colorful-label warn">评论189</span>
                        </div>
                    </div>
                    <div class="article-summary">
                        {{ article.summary}}
                    </div>
                </div>
            </a>
            <div>
                <el-button>
                    加载更多...
                </el-button>
            </div>


        </div>
        <el-backtop target=".article-list_container"></el-backtop>
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
        text-align: left;
    }

    .article-list_item-container {
        display: block;
    }

    .article-list_item-container:visited {

    }

    .article-list_item {
        margin: 0px 0px 15px 0px;;
        height: auto;
        border-radius: 5px;
        cursor: pointer;
        padding: 15px;
        background-color: #f0f0f0;
    }

    .article-list_item:hover {
        box-shadow: 0px 0px 6px gray;
    }

    .article-title {
        color: #2910b5;
        cursor: default;
        font-size: 1.3rem;
        padding: 5px 0px;
    }

    .article-summary {
        font-size: .9rem;
        margin-bottom: 10px;
        word-break: break-all;
        color: gray
    }

    .info-label {
        margin: 5px 0px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
    }

    .label-wrapper {
        padding: 0px 5px;
    }
</style>

