<template>
  <div>
    <el-card>
      <el-row justify="center">
        <h3>Report Details</h3>
      </el-row>
    </el-card>
    <el-card v-if="modifyFlag">
      <div >
        <div class="grid-content bg-purple-light">
          <el-input
            type="text"
            placeholder="Please input title"
            v-model="reportTitle"
            class="report-editarea"
          >
          </el-input>
        </div>
      </div>
      <br />
      <div>
        <div class="grid-content bg-purple-light">
          <el-input
            type="textarea"
            :rows="21"
            placeholder="Please Start Your Inspection report from Here"
            v-model="reportContent"
            class="report-editarea"
          >
          </el-input>
        </div>
        <br />
        <el-row type="flex" class="report-Header" justify="center">
          <el-button type="primary" round @click.prevent="UpdateReport"
            >Updating</el-button
          >
          <el-button type="danger" round @click="CancelUpdate()">Cancel</el-button>
        </el-row>
      </div>
    </el-card>
    <el-card v-else>
      <div >
        <div class="grid-content bg-purple-light">
          This is the Title
        </div>
      </div>
      <br />
      <div>
        <div class="grid-content bg-purple-light">
          This is the Content
        </div>
        <br />
        <el-row type="flex" class="report-Header" justify="center">
          <el-button type="primary" round @click.prevent="ModifyReport()"
            >Modify</el-button
          >
          <el-button type="danger" round @click="BackToOverview()">Back</el-button>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { extractDateFormat } from "element-plus";
import { Testurl } from "@/http";
import { inject } from 'vue'

export default {
  data() {
    return {
      modifyFlag: false,
      reportContent: this.content,
      reportTitle: this.title,
      reportDate: "",
    };
  },
  methods: {
    show(){
      console.log(topics)
      console.log(selectTopic)
    },
    ModifyReport(){
      this.modifyFlag =!this.modifyFlag
    },
    BackToOverview(){
      this.$router.push({ name: 'ReportOverview', query: { id: "1" } });
    },
    CancelUpdate(){
      this.modifyFlag = !this.modifyFlag
      // this.$router.push({ name: 'reportDetail', query: { id: "1" } });
    }
  },
};
</script>