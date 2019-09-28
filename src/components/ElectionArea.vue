<template>
  <span v-if="seats[null]">
    <router-link :to="{name: 'election', params: {id: seats[null]}}">
      <h3>{{ title }}</h3>
    </router-link>
  </span>
  <span v-else>
    <h3>{{ title }}</h3>
    <ul>
      <li :key="seat_name" v-for="(id, seat_name) in seats">
        <router-link :to="{name: 'election', params: {id}}">{{ seat_name }}</router-link>
      </li>
    </ul>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component()
export default class ElectionArea extends Vue {
  @Prop() private seats!: object;

  @Prop() private title!: string;
}
</script>


<style scoped lang="scss">

h3 {
  margin: 0;
  padding: 0;
  padding-bottom: .5em;
  padding-top: .25em;
}

ul {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  justify-content: space-evenly;
  align-content: flex-start;
  margin: 0;
  padding: 0;

  li {
    flex-grow: 1;
    display: block;
    margin: .25em;
    padding: .5em;
    border: 1px solid grey;
    border-radius: .5em;
  }
}

</style>
