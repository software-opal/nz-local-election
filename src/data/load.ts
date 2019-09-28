
import { named as rawNamed } from '@/assets/data_lookup.json';
import { Election } from './types';

const named: Map<string, string> = new Map(Object.entries(rawNamed));

const dataStore: Map<string, Promise<Election>> = new Map();

async function loadData(id: string): Promise<Election> {
  await Promise.resolve();
  const fname = named.get(id);
  if (!fname) {
    throw new Error(`Request for ${id} failed: Unknown ID`);
  }
  const resp = await fetch(`./data/${fname}`);
  if (!resp.ok) {
    throw new Error(`Request for ${id} failed: ${resp.status} ${resp.statusText}`);
  }
  const json = await resp.json();
  return Election.initialize(json);
}


export default function requestData(id: string) : Promise<Election> {
  let prom = dataStore.get(id);
  if (prom) {
    return prom;
  }
  prom = loadData(id);
  dataStore.set(id, prom);
  return prom;
}
