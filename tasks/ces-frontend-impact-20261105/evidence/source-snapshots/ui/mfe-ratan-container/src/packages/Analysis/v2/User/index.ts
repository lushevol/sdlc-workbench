import { encode } from "../Storage/crypto";
import {
  getUID,
  getLanguage,
  getTimeZone,
  getTimeZoneOffset,
  getUserAgent,
  getUserName,
  getUserEmail,
  getUserId,
  getUserCountry,
  getUserProfile,
} from "./utils";

export class MonitorUser {
  name: string;
  email: string;
  bid: string;
  uid: string;
  profile: string;
  country: string;
  tz: string;
  tzos: string;
  ua: string;
  lang: string;
  constructor() {
    this.name = encode(getUserName());
    this.email = encode(getUserEmail());
    this.bid = encode(getUserId());
    this.uid = getUID();
    this.country = getUserCountry();
    this.tz = getTimeZone();
    this.tzos = getTimeZoneOffset();
    this.ua = getUserAgent();
    this.lang = getLanguage();
    this.profile = getUserProfile();
  }
}
