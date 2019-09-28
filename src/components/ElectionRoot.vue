<template>
  <span>
    <h2>{{ title }}</h2>
    <ul>
      <li :key="council_name" v-for="(seats, council_name) in data">
        <ElectionArea :title="council_name" :seats="seats" />
      </li>
    </ul>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ElectionArea from './ElectionArea.vue';

@Component({
  components: {
    ElectionArea,
  },
})
export default class ElectionRoot extends Vue {
  @Prop() private data!: object;

  @Prop() private title!: string;
}
</script>

<style scoped lang="scss">
$card-size: 18rem;

h2 {
  margin: 0;
  padding: 0;
  padding-bottom: .5em;
  padding-top: 1em;
}

ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  justify-content: space-evenly;
  align-items: stretch;
  align-content: flex-start;
  margin: 0;
  padding: 0;

  li {
    flex-grow: 1;
    display: block;
    margin: .5em;
    padding: 0;
    width: $card-size;
    border: 1px solid grey;
    border-radius: .5em;

    @media screen and (max-width: $card-size) {
      width: 100%;
    }
  }
}
</style>
