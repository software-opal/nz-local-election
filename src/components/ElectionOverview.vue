<template>
  <div>
    <h1>Sort out your votes for the 2019 Local Government elections</h1>
    <div>
      Voting is done in 4 seperate elections:
      <ElectionRoot title="City Council Mayor" :data="data['Mayor']" />
      <ElectionRoot title="City Council Councillors" :data="data['City Councillor']" />
      <ElectionRoot title="Regional Council Councillors" :data="data['Regional Councillor']" />
      <ElectionRoot title="District Health Board Members" :data="data['DHB']" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ElectionRoot from './ElectionRoot.vue';

@Component({
  components: {
    ElectionRoot,
  },
})
export default class ElectionOverview extends Vue {
  @Prop() private data!: object;
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h1 {
  margin: 40px 0 0;
}
</style>
