fn main() {
    let schemas = match std::env::args().nth(1).as_deref() {
        Some("--requests") => waypoint_traces::schema::request_schemas(),
        Some("--responses") => waypoint_traces::schema::response_schemas(),
        _ => waypoint_traces::schema::schemas(),
    };
    println!("{}", serde_json::to_string_pretty(&schemas).unwrap());
}
