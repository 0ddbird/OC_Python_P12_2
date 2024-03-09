use std::env;
use std::fs;
use std::sync::{Arc, Mutex};
use tokio::net::UnixListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use dotenv::dotenv;


#[tokio::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();

    let socket_path = env::var("SOCKET_PATH").unwrap();
    let token = Arc::new(Mutex::new(None::<String>));

    if fs::metadata(&socket_path).is_ok() {
        fs::remove_file(&socket_path)?;
    }

    let listener = UnixListener::bind(&socket_path)?;

    println!("Server started and listening on {}", &socket_path);

    loop {
        let (mut socket, _) = listener.accept().await?;
        let token_clone = Arc::clone(&token);

        tokio::spawn(async move {
            let mut buf = vec![0; 1024];
            socket.read(&mut buf).await.unwrap();
            let message = String::from_utf8(buf).unwrap();
            let message = message.trim_matches(char::from(0));
            if message == "get_token" {
                let response = match &*token_clone.lock().unwrap() {
                    Some(token) => token.clone(),
                    None => "No token stored".to_string(),
                };
                socket.write_all(response.as_bytes()).await.unwrap();
            } else {
                *token_clone.lock().unwrap() = Some(message.to_string());
                let response = "Token stored";
                socket.write_all(response.as_bytes()).await.unwrap();
            }
        });
    }
}