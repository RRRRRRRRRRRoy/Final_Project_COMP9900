<template>
  <div>
    <div id="refresh">
      <el-button icon="el-icon-location" circle @click="refresh" />
    </div>
    <el-row
      @click="refresh"
      justify="center"
      style="height: 40px; font-size: 20px; font-weight: bold; cursor: pointer"
      >{{ place.formatted_address }}</el-row
    >
    <div id="showMap" style="height: 300px; width: 100%" />
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  props: {
    place: Object,
  },
  data() {
    return {
      map: ref(null),
    };
  },
  methods: {
    refresh() {
      if (this.place.geometry.viewport) {
        this.map.fitBounds(this.place.geometry.viewport);
      } else {
        this.map.setCenter(this.place.geometry.location);
        this.map.setZoom(20);
      }
      marker.setPosition(this.place.geometry.location);
    },
  },
  beforeMount() {},
  mounted: function () {
    this.map = new google.maps.Map(document.getElementById("showMap"), {
      zoom: 10,
      center: { lat: -33.85, lng: 151.11 },
      fullscreenControl: false,
      zoomControl: false,
      streetViewControl: false,
    });
    const button = document.getElementById("refresh");
    this.map.controls[google.maps.ControlPosition.TOP_RIGHT].push(button);
    let marker = new google.maps.Marker({
      map: this.map,
    });
    if (this.place.geometry.viewport) {
      this.map.fitBounds(this.place.geometry.viewport);
    } else {
      this.map.setCenter(this.place.geometry.location);
      this.map.setZoom(20);
    }
    marker.setPosition(this.place.geometry.location);
  },
};
</script>
