{% raw %}
<template id="chrome-plugin-list">
    <div style="height: 100%;width:100%;display: flex;justify-content: center;">
        <div style="width: 70%;height: 100%;background-color: #f0f0f0;box-shadow: 0px 0px 2px gray" v-loading="loading">
            <div class="plugin-list-container">
                <a :href="'/chrome-plugin/detail/'+plugin.id" v-for="plugin in plugins">
                    <div class="plugin-list-item">
                        <img aria-hidden="true"
                             :src="plugin.cover_image"
                             class="plugin-list-item-cover-img">
                        <div class="plugin-list-item-description">
                            {{ plugin.short_desc }}
                        </div>
                        <div class="plugin-list-item-info">
                            {{ plugin.name }}
                        </div>
                    </div>
                </a>
            </div>
            <pagination :total="total" :size_change="sizeChange" :current_change="list" :page_size="20"></pagination>
        </div>
    </div>
</template>
{% endraw %}
{% include 'base/pagination.vue' %}
<script>
    Vue.component("main-content", {
        template: "#chrome-plugin-list",
        data() {
            return {
                plugins: [],
                loading: false,
                pageSize: 20,
                total: 0
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
                this.$http.get("/chrome-plugin/list-data", {
                    params: assign
                }).then(res => {
                    this.plugins = res.data.list
                    this.total = res.data.total
                    this.loading = false
                }).catch(e => {

                    this.loading = false
                })
            },
            sizeChange(s) {
                this.pageSize = s
                this.list(0, {pageSize: s})
            }
        }
    });
</script>
<style>

    .plugin-list-container {
        display: flex;
        align-content: center;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        padding-right: 25px;
    }

    .plugin-list-item {
        height: auto;
        display: inline-block;
        margin-left: 25px;
        align-self: flex-start;
        margin-top: 25px;
        width: 215px;
        color: #3c4043;
        position: relative;
    }


    .plugin-list-item-cover-img {
        border: 0;
        left: 0;
        margin: 0;
        top: 0;
        width: 215px;
        height: 140px;
        position: static;
    }

    .plugin-list-item-description {
        opacity: 0;
        position: absolute;
        align-items: center;
        box-sizing: border-box;
        display: flex;
        height: 140px;
        justify-content: center;
        left: 0;
        padding: 10px;
        text-align: center;
        top: 0;
        width: 215px;

        letter-spacing: .01428571em;
        font-family: Roboto, Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
        background-color: rgba(255, 255, 255, 0.95);
        z-index: 3;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: pointer;
    }

    .plugin-list-item-description:hover {
        opacity: 1;
        transition: 0.5s;
    }

    .plugin-list-item-info {
        margin-top: 15px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .plugin-list-item-info-name {
        left: auto;
        top: auto;
        width: 100%;
        letter-spacing: 0.2px;
        font-family: 'Google Sans', Roboto, Arial, sans-serif;
        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
        max-height: none;
        position: static;
        word-break: break-word;
    }

    /*plugin_detail.html*/
    .plugin-detail-container {
        /*background-color: white;*/
        padding: 10px;
    }

    #carouselExampleIndicators {
        width: 480px;
        margin: auto;
        height: 300px;
    }

</style>

