<template>
  <ElectionOverview :data="groups"/>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ElectionOverview from '@/components/ElectionOverview.vue'; // @ is an alias to /src
import lookupData from '@/assets/data_lookup.json';

@Component({
  components: {
    ElectionOverview,
  },
})
export default class Home extends Vue {
  @Prop({ default: lookupData.grouped }) private groups!: object;
}
</script>
