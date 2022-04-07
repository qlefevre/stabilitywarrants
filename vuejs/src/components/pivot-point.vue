<template>
  <div class="pivotpoint">
    <div class="libelle">{{ this.value.period }}</div>
    <div class="support">S3:</div>
    {{ this.value.pivotpoint.S3 }}
    <div class="support">S2:</div>
    {{ this.value.pivotpoint.S2 }}
    <div class="support">S1:</div>
    {{ this.value.pivotpoint.S1 }}
    <div class="pivot">Pivot:</div>
    {{ this.value.pivotpoint.P }}
    <div class="resistance">R1:</div>
    {{ this.value.pivotpoint.R1 }}
    <div class="resistance">R2:</div>
    {{ this.value.pivotpoint.R2 }}
    <div class="resistance">R3:</div>
    {{ this.value.pivotpoint.R3 }}
  </div>
</template>

<script>
module.exports = {
  props: ["value"],
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
  width: 90px;
}
.pivotpoint div {
  padding: 0px 5px 0px 12px;
  display: inline-block;
}
.pivotpoint {
  margin: 0 auto;
  width: auto;
  margin-bottom: 5px;
}
</style>