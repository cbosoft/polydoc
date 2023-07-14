const state = {
    session_id: null,
};

/// initialise web app state
function init() {
    state.session_id = Date.now();
}


/// Simple function to POST an object as JSON to the server
/// sent data is handled by the [WebRequestHandler::do_POST](multi/server/server.py|Method:WebRequestHandler/do_POST) method.
/// params:
///     - o :: the object to be sent
/// returns:
///     - promise of response object
export function send_data(o) {
    return fetch('/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(o)
    })
    .then(r => r.json());
}