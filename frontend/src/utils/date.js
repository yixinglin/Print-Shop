import moment from 'moment';

export function formatDateToLocal(utcString, format) {
    return moment(utcString).format(format);
}