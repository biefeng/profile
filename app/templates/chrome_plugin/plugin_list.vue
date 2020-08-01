{% raw %}
<template id="chrome-plugin-list">
    <div>
        <div role="grid" class="plugin-list-container" v-loading="loading">
            <el-select v-model="category">
                <el-option v-for="item in categories"
                           :key="item.value"
                           :label="item.label"
                           :value="item.value">
                </el-option>
            </el-select>
            <el-input v-model="searchKey" placeholder="" suffix-icon="el-icon-search"></el-input>
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
            <pagination v-if="plugins.length>0" :total="total" :size_change="sizeChange" :current_change="list" :page_size="20"></pagination>
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
                total: 0,
                categories: [
                    {
                        label: '生产工具', value: 1
                    }, {
                        label: '开发者工具', value: 0
                    }
                ],
                category: 0,
                searchKey: ''
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
                }).finally(() => {
                    document.title = "Chrome 插件,Crx文件下载";
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
        padding-right: 25px;
        background-color: #f0f0f0;
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


</style>

