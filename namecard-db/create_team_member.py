"""
建立/更新團隊成員帳號，供名片跟進紀錄簿登入用。

互動模式（推薦，密碼不會顯示在畫面或log上）：
    python3 create_team_member.py --username peipei --display-name 佩佩老師

非互動模式（給自動化流程用，密碼會出現在指令歷史，較不安全）：
    python3 create_team_member.py --username peipei --display-name 佩佩老師 --password xxx
"""
import argparse
import getpass

from werkzeug.security import generate_password_hash

import db


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--display-name", default="")
    parser.add_argument("--password", default=None, help="不帶此參數時會用互動方式安全輸入")
    args = parser.parse_args()

    password = args.password or getpass.getpass(f"設定 {args.username} 的登入密碼：")
    if not password:
        raise SystemExit("密碼不能空白")

    db.init_db()
    conn = db.get_conn()
    existing = db.get_team_member(conn, args.username)
    password_hash = generate_password_hash(password)
    if existing:
        conn.execute(
            "UPDATE team_members SET password_hash = ?, display_name = ? WHERE username = ?",
            (password_hash, args.display_name or existing["display_name"], args.username),
        )
        conn.commit()
        print(f"已更新帳號 {args.username} 的密碼")
    else:
        conn.execute(
            "INSERT INTO team_members (username, password_hash, display_name) VALUES (?, ?, ?)",
            (args.username, password_hash, args.display_name or args.username),
        )
        conn.commit()
        print(f"已建立新帳號 {args.username}（{args.display_name or args.username}）")
    conn.close()


if __name__ == "__main__":
    main()
