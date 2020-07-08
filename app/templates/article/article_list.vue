{% raw %}
<template id="article_list">

    <div class="article-list_container" v-loading="loading">
        <a class="article-list_item-container" v-for="article in articles" :href="'/article/detail-view/'+article.id">
            <div class="article-list_item">
                <div class="article-title">{{article.title}}</div>

                <div style="margin-bottom: 10px;display: flex;align-items: center;flex-wrap: wrap;">
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


                    <!--<el-row type="flex">
                        <el-col :lg="3" :sm="3" :xs="8" :md="20">
                            <span class="colorful-label primary">
                                {{article.create_time}}
                            </span>
                        </el-col>
                        <el-col :lg="3" :sm="20" :xs="3" :md="20">
                            <span class="colorful-label warn">
                                {{article.source}}
                            </span>
                        </el-col>
                        <el-col :lg="3" :sm="20" :xs="3" :md="20">
                            <span class="colorful-label info">
                                未分类
                            </span>
                        </el-col>
                        <el-col :lg="{span:3,offset:8}" :xs="{span:6}">
                            <span class="colorful-label hot">
                                浏览数{{article.num_of_view}}
                            </span>
                        </el-col>
                        <el-col :lg="{span: 3,offset: 1}" :xs="{span:5}">
                            <span class="colorful-label warn">
                                评论189
                            </span>
                        </el-col>
                    </el-row>-->
                </div>
                <div class="article-summary">
                    {{ article.summary}}
                </div>
            </div>
        </a>
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
        color: #007bff;
        cursor: default;
        font-size: 1.5rem;
        height: 2.8rem;
        line-height: 2.8rem;
    }

    .article-summary {
        font-size: 1rem;
        margin-bottom: 10px;
        word-break: break-all;
        color: gray
    }

    .label-wrapper {
        padding: 2px 5px;
    }
</style>

