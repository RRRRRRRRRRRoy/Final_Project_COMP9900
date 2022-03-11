<template>
  <div>
    <el-progress
      :percentage="passwordIntensity"
      :color="colors"
      :show-text="false"
    />
    <div :style="{color: textColor, 'font-size': '10px'}">
      <div>Your password should be</div>
      <div>
        <i
          v-if="password.length < 21 && password.length > 7"
          class="el-icon-success"
        />
        <i v-else class="el-icon-error" style="color: red" />
        &nbsp;8~20 characters;
      </div>
      <div>
        <i v-if="/[A-Z]/.test(password)" class="el-icon-success" />
        <i v-else class="el-icon-error" style="color: red" />&nbsp; including at
        least an uppercase letter;
      </div>
      <div>
        <i v-if="/[a-z]/.test(password)" class="el-icon-success" />
        <i v-else class="el-icon-error" style="color: red" />&nbsp; including at
        least a lowercase letter;
      </div>
      <div>
        <i v-if="/[0-9]/.test(password)" class="el-icon-success" />
        <i v-else class="el-icon-error" style="color: red" />&nbsp; including at
        least a digit;
      </div>
      <div>
        <i
          v-if="
            /([\!\@\#\$\%\^\&\*\(\)\_\=\|\{\}\:\<\>\?\-\=\[\]\;\,\.\/\~])+/.test(
              password
            )
          "
          class="el-icon-success"
        />
        <i v-else class="el-icon-error" style="color: red" />&nbsp; including at
        least a symbol.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    password: String,
    passwordIntensity: Number,
    textColor: String,
  },
  data() {
    return {
      colors: [
        { color: "#909399", percentage: 30 },
        { color: "#F56C6C", percentage: 50 },
        { color: "#E6A23C", percentage: 70 },
        { color: "#409EFF", percentage: 90 },
        { color: "#67C23A", percentage: 100 },
      ],
    };
  },
};
</script>

<style scoped>
</style>