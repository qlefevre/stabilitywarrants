<template>
  <div class="pivotpoint">
    <span class="support">S3:</span> {{ this.value.S3 }}
    <span class="support">S2:</span> {{ this.value.S2 }}
    <span class="support">S1:</span> {{ this.value.S1 }}
    <span class="pivot">Pivot:</span> {{ this.value.P }}
    <span class="resistance">R1:</span> {{ this.value.R1 }}
    <span class="resistance">R2:</span> {{ this.value.R2 }}
    <span class="resistance">R3:</span> {{ this.value.R3 }}
  </div>
</template>

<script>
module.exports = {
  props: ["value"]
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
.pivotpoint span {
  padding: 0px 5px 0px 20px;
}
.pivotpoint {
  margin: 0 auto;
  width: auto;
}
</style>