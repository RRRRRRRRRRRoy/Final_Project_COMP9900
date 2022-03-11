<template>
    <div>
        <div>
            <el-row type="flex" class="properties-information" justify="center">
                <el-col :span="8">
                    <el-card class="property-box-card" justify="center">
                        <h3>  picture </h3>
                        <el-row type="flex" class="properties-info" justify="center">
                            <el-col class='uploading-img'>
                                    <el-upload
                                        action="https://jsonplaceholder.typicode.com/posts/"
                                        list-type="picture-card"
                                        :on-preview="handlePictureCardPreview"
                                        :on-remove="handleRemove">
                                            <i class="el-icon-plus" style="width:100%, height:450px"></i>
                                    </el-upload>
                                    <el-dialog :visible.sync="dialogVisible">
                                        <img width="100%" :src="dialogImageUrl" alt="">
                                    </el-dialog>
                            </el-col>    
                        </el-row>
                    </el-card>
                </el-col>
                <el-col :span="10">
                        <el-card class="property-box-card" justify="center">
                        <h3>  Property information </h3>
                        <div class = "properties-information">
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Renter Name:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                    v-model="renterName"
                                    placeholder="Renter Name"
                                    clearable
                                />
                                </el-col>
                            </el-row>
                            <br> 
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Renter Tel.:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                    v-model="renterTel"
                                    placeholder="Renter Tel."
                                    clearable
                                />
                                </el-col>
                            </el-row>
                            <br>
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Renter Email:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                    v-model="renterEmail"
                                    placeholder="Renter Email Address"
                                    clearable
                                />
                                </el-col>
                            </el-row>
                            <br> 
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Property Address:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                    v-model="propertiesAddress"
                                    placeholder="Properties Address"
                                    clearable
                                />
                                </el-col>
                            </el-row>
                            <br>  
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Rent Start Date:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                        v-model="rentStartDate"
                                        placeholder="Rent Start Date"
                                        suffix-icon="el-icon-date"
                                        clearable
                                    />
                                </el-col>
                            </el-row> 
                            <br>
                            <el-row type="flex" justify="center">
                                <el-col :span="5" style="font-size:20px">
                                    Rent End Date:
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                    v-model="rentEndDate"
                                    placeholder="Rent End Date"
                                    suffix-icon="el-icon-date"
                                    clearable
                                />
                                </el-col>
                            </el-row> 
                            <br>
                            <el-row type="flex" justify="center">
                                <el-button type="primary" round style="font-family:'Times New Roman', Times, serif;">
                                    Show location
                                </el-button>
                                <el-button type="success" round style="font-family:'Times New Roman', Times, serif;">
                                    Submit Information
                                </el-button>
                                <el-button type="danger" round style="font-family:'Times New Roman', Times, serif;">
                                    Clear Information
                                </el-button>
                            </el-row>                  
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </div>
        <div>
            <el-row type="flex" class="properties-location" justify="center">
                    <el-col :span="18">
                        <el-card class="box-card" justify="center">
                            <h3> Google Map location</h3>
                            <!-- <div class="properties-location"></div> -->
                            <!-- AIzaSyD0_U300oQdbD1_lJ70uhH_T1ybMkyTxe0   -->
                            <GoogleMap
                                class='Google-map'
                                api-key=""
                                :center="center"
                                :zoom="15"
                                >
                                <Marker :options="{ position: center }" />
                        </GoogleMap>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import { GoogleMap, Marker } from 'vue3-google-map'

export default defineComponent({
  components: { GoogleMap, Marker },
  setup() {
    const center = { lat: -33.8688197000, lng: 151.2092955000 }

    return { center }
  },
  data(){
      return {
        dialogImageUrl: '',
        dialogVisible: false,
        renterName: "",
        renterTel: "",
        renterEmail: "",
        propertiesAddress: "",
        rentStartDate: "",
        rentEndDate:""
      };
  },
  methods:{
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },

  }
})
</script>



<style scoped>
.html{
    font-family:'Times New Roman', Times, serif;
}
.property-box-card{
    width:100%;
    height: 550px;
}

.uploading-img {
    display:flex;
    justify-content: center;
    text-align: center;
}


h3{
    display:flex;
    justify-content:center;
    font-size: 25px;
    font-family:'Times New Roman', Times, serif;
    font-weight: bold;
}

.tenant-info{
    display:flex;
    justify-content:center;
}

.Google-map{
    width: 100%;
    height: 450px;
}

</style>