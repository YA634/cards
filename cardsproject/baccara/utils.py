from .models import RoadMap

def update_roadmap(user, winner):

    
    # 最新の罫線を取得
    last_roadmap = RoadMap.objects.filter(user=user).order_by('-column_position').first()
    
    if winner == 'tie':
        # tie_po = last_roadmap.consecutive_count
        if last_roadmap:
            # 現在の位置（連勝回数 + 1）に引き分けを記録
            current_position = last_roadmap.consecutive_count
            last_roadmap.tie_positions.append(current_position)
            last_roadmap.save()
        # 最初のゲームが引き分けの場合は何もしない
        return

    elif last_roadmap and last_roadmap.winner == winner:
        # 前回と同じ勝者なら、連勝回数を増やす
        last_roadmap.consecutive_count += 1
        last_roadmap.save()
    else:
        # 前回と違う勝者なら、新しい列を作る
        next_position = last_roadmap.column_position + 1 if last_roadmap else 0
        RoadMap.objects.create(
            user=user,
            winner=winner,
            consecutive_count=1,
            tie_positions=[],
            column_position=next_position
        )




def get_roadmap_display(user, limit=50):

    # 罫線を表示用のデータに変換
    # limit: 表示する列数の上限

    roadmaps = RoadMap.objects.filter(user=user).order_by('column_position')[:limit]
    
    display_data = []
    for roadmap in roadmaps:
        symbol = '🔴' if roadmap.winner == 'banker' else '🔵'

        display_data.append({
            'winner': roadmap.winner,
            'count': roadmap.consecutive_count,
            'tie_positions': roadmap.tie_positions,  # [1, 3] のような形式
            'symbol': symbol
        })
    
    return display_data