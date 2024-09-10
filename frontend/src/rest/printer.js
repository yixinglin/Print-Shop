
import axios from 'axios';


const domain = import.meta.env.VITE_API_URL;
const port = import.meta.env.VITE_API_PORT;
const apiUrl = `http://${domain}:${port}/cups`;
const wsUrl = `ws://${domain}:${port}/cups/ws`;
const cupsUrl = `http://${domain}:631`;

function calc_token() {
    const username = import.meta.env.VITE_API_USERNAME;
    const password = import.meta.env.VITE_API_PASSWORD;    
    const token = btoa(`${username}:${password}`);
    return token;
}


function get_method(url) { 
    const headers = {};
    headers['Authorization'] = `Basic ${calc_token()}`;    
    headers['Content-Type'] = 'application/json';
    return axios.get(url, { headers: headers });
}

function post_method(url, body) { 
    const headers = {};
    headers['Authorization'] = `Basic ${calc_token()}`;    
    headers['Content-Type'] = 'application/json';
    return axios.post(url, body, { headers: headers });
}

export function fetch_printers() {
    return get_method(apiUrl + '/printers');
}

export function fetch_printer(id) {
    return get_method(apiUrl + '/printers/' + id);
}

export function fetch_printer_status(printer) {
    return get_method(apiUrl + '/status/' + printer);
}

export function fetch_printer_attributes(printer) {
    return get_method(apiUrl + '/attributes/' + printer);
}

export function fetch_jobs() {
    return get_method(apiUrl + '/jobs');
}

export function fetch_job_attributes(id) {
    return get_method(apiUrl + `/jobs/${id}`);
}

export function delete_all_jobs() {
    return delete_method(apiUrl + '/jobs/cancel/all/');
}

export function get_cups_admin_url() {
    return cupsUrl;
}

export function get_printer_status_ws_listener_url(printer) {
    return `${wsUrl}/printer/${printer}`;
}

/**
 * 
  File System Operations
 */

export function post_create_job(body) {
    return post_method(apiUrl + '/jobs/create/from_history', body);
}

export function fetch_list_history_files({include_archived}) {    
    return get_method(apiUrl + '/history/files?include_archived=' + include_archived);
}

export function post_upload_file(body) {
    return post_method(apiUrl + '/history/upload/', body, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }
    )
}

export function get_upload_file_url() {
    return apiUrl + '/history/upload/';
}


function delete_method(url) {
    const headers = {};
    headers['Authorization'] = `Basic ${calc_token()}`;    
    headers['Content-Type'] = 'application/json';
    return axios.delete(url, { headers: headers });
}

function put_method(url, body) {
    const headers = {};
    headers['Authorization'] = `Basic ${calc_token()}`;    
    headers['Content-Type'] = 'application/json';
    return axios.put(url, body, { headers: headers });
}

export function delete_file(hash) {
    return delete_method(apiUrl + '/history/file/archive/' + hash);
}

export function delete_all_files() {
    return delete_method(apiUrl + '/history/file/archive-all');
}

export function restore_file(hash) {
    return put_method(apiUrl + '/history/file/unarchive/' + hash, {});
}

export function get_download_file_url(hash, embedded, enabled_watermark) {
    var url = apiUrl + '/history/file/down/' + hash;
    url += `?embedded=${embedded}&enabled_watermark=${enabled_watermark}`
    return url;
}

export function accumulate_file_print_count(hash) {
    return put_method(apiUrl + '/history/file/print-count/1/' + hash, {});
}
