{%raw%}
<template id="sample">

    <div class="plugin-detail-container">
        <div class="plugin-name">{{ plugin.name }}</div>
        <div class="carousel-container">
            <el-carousel>
                <el-carousel-item v-for="item in 3" :key="item">
                    <img class="plugin-cover-image" :src="plugin.cover_image"/>
                </el-carousel-item>
            </el-carousel>
        </div>
        <div class="plugin-detail-description">
            <div style="width: 100%;text-align: right;padding-right: 30px">
                <el-button @click="download(plugin.crx_url)" type="primary">下载</el-button>

            </div>
            <div style="white-space: pre-line;font-size: 16px;line-height: 24px;">

                <div style="font-weight: bolder;">{{ plugin.short_desc }}</div>
                <div style="font-weight: 300;">{{ plugin.description }}</div>
            </div>
        </div>
    </div>

</template>
{%endraw%}
<script>
    console.log(window.context)
    Vue.component("main-content", {
        template: "#sample",
        data() {
            return {
                message: "The is a sample component",
                id: '{{id}}', //由jinja模板去解析并赋值
                plugin: {}
            }
        },
        created() {
            this.getDetail()
        },
        methods: {
            getDetail() {
                this.$http.get("/chrome-plugin/detail-data/" + this.id).then(res => {
                    if (res.data) {
                        this.plugin = res.data
                        document.title = res.data.title
                    } else {
                        document.title = 'Not found'
                    }
                })
            },
            download(url, filename) {
                let element = document.createElement("a");
                element.href = url
                // element.download = filename
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                this.$http.get("/download-count/" + this.id).then(res => {
                    //
                })
            }
        }
    });
</script>
<style>
    .carousel-container {
        width: 330px;
        height: 210px;
        margin: auto
    }

    .plugin-name {
        font-size: 30px;
        margin: 0 0 0 10px;
        font-weight: 400;
        text-align: left;
    }

    .plugin-detail-container {
        height: 100%;
        padding-bottom: 10px;
        background-color: #f0f0f0;
    }

    .el-carousel__container {
        height: 200px;
    }

    .plugin-cover-image {
        width: 330px;
        height: 210px;
    }

    .plugin-detail-description {
        text-align: left;
        margin: 0px 10px 0px 10px;
    }

    @media screen and (min-width: 768px) {
        .carousel-container {
            width: 440px;
            height: 280px;
        }

        .plugin-name {
            margin: 0px 0 0 50px;
        }

        .el-carousel__container {
            height: 300px;
        }

        .plugin-cover-image {
            width: 440px;
            height: 280px;
        }

        .plugin-detail-description {
            text-align: left;
            margin: 0px 50px 0px 50px;
        }
    }


</style>

