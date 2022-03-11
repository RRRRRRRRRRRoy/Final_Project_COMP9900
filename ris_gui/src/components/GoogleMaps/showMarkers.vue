<template>
  <div>
    <div id="reset">
      <el-button @click="reset">Reset</el-button>
    </div>
    <div>Click the address to make map focus</div>
    <div v-for="(value, key) in places" :key="key">
      <div
        v-if="value"
        style="cursor: pointer; font-weight: bold; color: darkgreen"
        @click="focus(value)"
      >
        Address {{ key }}: {{ value.formatted_address }}
      </div>
    </div>
    <div id="map" style="height: 350px; width: 100%" />
  </div>
</template>

<script>
import { ref, reactive } from "vue";
export default {
  props: {
    places: Object,
  },
  data() {
    return {
      map: ref(null),
      bounds: ref(null),
      count: ref(0),
    };
  },
  methods: {
    reset() {
      if (this.count > 1) {
        this.map.fitBounds(this.bounds);
        this.map.setCenter(this.bounds.getCenter());
      } else {
        this.map.setZoom(18);
      }
      this.map.setCenter(this.bounds.getCenter());
    },
    focus(value) {
      this.map.setCenter(value.loc);
      this.map.setZoom(18);
    },
  },
  mounted: function () {
    this.map = new google.maps.Map(document.getElementById("map"), {
      zoom: 10,
      streetViewControl: false,
    });
    const button = document.getElementById("reset");
    this.map.controls[google.maps.ControlPosition.TOP_RIGHT].push(button);
    this.bounds = new google.maps.LatLngBounds();
    for (let i in this.places) {
      if (this.places[i]) {
        this.count += 1;
        this.bounds.extend(this.places[i].loc);
      }
    }
    for (let i in this.places) {
      if (this.places[i]) {
        new google.maps.Marker({
          map: this.map,
          position: this.places[i].loc,
          title: this.places[i].formatted_address,
          animation: google.maps.Animation.DROP,
          label: i,
        });
      }
    }
    if (this.count > 1) {
      this.map.fitBounds(this.bounds);
      this.map.setCenter(this.bounds.getCenter());
    } else {
      this.map.setZoom(18);
    }
    this.map.setCenter(this.bounds.getCenter());
  },
};
</script>

