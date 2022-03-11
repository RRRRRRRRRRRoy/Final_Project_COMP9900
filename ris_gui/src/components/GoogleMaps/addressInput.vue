<template>
  <div>
    <el-alert
      v-if="wrongAddr"
      title="The address does not exist."
      type="error"
      effect="dark"
    />
    <el-input
      style="width: 100%"
      ref="autocomplete"
      :id="id"
      placeholder="Type to edit the address"
      v-model="autocompleteText"
      clearable
      @clear="clearAddr"
    />
    <el-dialog
      v-model="showGMap"
      destroy-on-close
      width="40%"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <template #title
        ><span style="font-size: 20px; font-weight: bold">
          Confirm your address</span
        >
      </template>
      <show-map :place="places" />
      <template #footer>
        <el-button
          type="danger"
          @click="cancelEditAddr"
          style="width: 150px"
          plain
          >Cancel</el-button
        >
        <el-button
          type="success"
          @click="confirmEditAddr"
          style="width: 150px"
          plain
          >Confirm</el-button
        >
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import ShowMap from "./showMap.vue";
export default {
  components: { ShowMap },
  props: {
    id: String,
  },
  data() {
    return {
      autocomplete: ref(null),
      wrongAddr: ref(false),
      showGMap: ref(false),
      autocompleteText: ref(""),
      fields: ["formatted_address", "geometry"],
      location: reactive({
        loc: {
          lat: 0,
          lng: 0,
        },
        formatted_address: "",
      }),
      places: ref(null),
    };
  },
  mounted: function () {
    this.autocomplete = new google.maps.places.Autocomplete(
      document.getElementById(this.id),
      {
        componentRestrictions: { country: "AU" },
      }
    );
    this.autocomplete.setFields(this.fields);
    this.autocomplete.addListener("place_changed", this.onPlaceChanged);
  },
  methods: {
    onPlaceChanged() {
      this.wrongAddr = false;
      this.showGMap = false;
      let place = this.autocomplete.getPlace();
      if (!place.geometry) {
        this.wrongAddr = true;
        return;
      }
      this.places = place;
      this.showGMap = true;
      this.autocompleteText = document.getElementById(this.id).value;
    },
    confirmEditAddr() {
      this.location.loc.lat = this.places.geometry.location.lat();
      this.location.loc.lng = this.places.geometry.location.lng();
      this.location.formatted_address = this.places.formatted_address;
      this.$emit("get-address", this.location, this.id);
      this.showGMap = false;
    },
    cancelEditAddr() {
      this.places = null;
      // this.$emit("get-address", "", this.id);
      this.autocompleteText = "";
      this.showGMap = false;
    },
    clearAddr(){
      this.$emit('clear-address')
    }
  },
};
</script>

<style scoped>
</style>