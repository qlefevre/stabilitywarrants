<template>
  <div class="pivotpoint">
    <div class="libelle">{{ this.value.period }}</div>
    <div class="support">S3:</div>
    {{ this.value.pivotpoint.S3 }}
    <div class="support hidden-md-and-down">mS3:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.S3, this.value.pivotpoint.S2) }}</div>
    <div class="support">S2:</div>
    {{ this.value.pivotpoint.S2 }}
    <div class="support hidden-md-and-down">mS2:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.S2, this.value.pivotpoint.S1) }}</div>
    <div class="support">S1:</div>
    {{ this.value.pivotpoint.S1 }}
    <div class="support hidden-md-and-down">mS1:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.S1, this.value.pivotpoint.P) }}</div>
    <div class="pivot">Pivot:</div>
    {{ this.value.pivotpoint.P }}
    <div class="resistance hidden-md-and-down">mR1:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.P, this.value.pivotpoint.R1) }}</div>
    <div class="resistance">R1:</div>
    {{ this.value.pivotpoint.R1 }}
    <div class="resistance hidden-md-and-down">mR2:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.R1, this.value.pivotpoint.R2) }}</div>
    <div class="resistance">R2:</div>
    {{ this.value.pivotpoint.R2 }}
    <div class="resistance hidden-md-and-down">mR3:</div>
    <div class="value hidden-md-and-down">{{ this.middle(this.value.pivotpoint.R2, this.value.pivotpoint.R3) }}</div>
    <div class="resistance">R3:</div>
    {{ this.value.pivotpoint.R3 }}
  </div>
</template>

<script>
module.exports = {
  props: ["value"],
  methods: {
    middle: function (middle0, middle1) {
      return Math.round((middle0 + middle1) / 2);
    },
  },
};
</script>

<style>
.support {
  color: red;
}
.pivot {
  color: blue;
}
.resistance {
  color: green;
}
.pivotpoint div.libelle {
  text-align: right;
  width: 78px;
}
.pivotpoint div {
  padding: 0px 5px 0px 12px;
  display: inline-block;
}
@media (max-width: 960px) {
  .pivotpoint div {
    padding: 0px 2px 0px 4px;
  }
}
.pivotpoint div.value {
  padding: 0px;
  display: inline-block;
}
.pivotpoint {
  margin: 0 auto;
  width: auto;
  margin-bottom: 5px;
}
</style>